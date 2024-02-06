from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from order.models import Order, OrderItems, Review
import datetime
from datetime import timedelta
from django.utils import timezone
import random
from product.models import ProductVarient
from security.models import CustomUser
from userdetails.models import Address
from django.views.decorators.cache import cache_control

# Create your views here.


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def order(request):
    temp = request.user
    user = CustomUser.objects.get(username=temp)
    items = Order.objects.filter(user=user)
    context = {
        'items': items
    }

    return render(request, 'order/order.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def checkout(request):
    temp = request.user
    user = CustomUser.objects.get(username=temp)
    cart = Cart.objects.filter(user=user)
    if cart:

        userwallet = user.wallet
        address = Address.objects.filter(user=user)

        if request.method == "POST":
            deliveryaddressid = request.POST.get('address')
            paymentmethod = request.POST.get('paymentmethod')
            wallet = request.POST.get('wallet')
            context = {
                "address": deliveryaddressid,
                'paymentmethod': paymentmethod,
                'wallet': wallet
            }
            request.session['order'] = context

            return redirect('confirm')
        context = {
            "address": address,
            'userwallet': userwallet
        }
        return render(request, 'order/checkout.html', context)
    else:
        return redirect('offers')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def confirm(request):
    if 'order' in request.session:
        address = request.session.get('order')
        paymentmethod = address['paymentmethod']
        addressid = address['address']
        usewallet = address['wallet']

        temp = request.user
        user = CustomUser.objects.get(username=temp)
        items = Cart.objects.filter(user=user)

        grandtotal = 0
        for i in items:
            if i.product.quantity > 0:
                grandtotal += i.totalprice()

        delivercharge = 0
        if grandtotal < 1000:
            delivercharge += 70
            grandtotal += 70

        wallet = 0
        if usewallet:
            if user.wallet > grandtotal:
                wallet = grandtotal
            elif user.wallet < grandtotal:
                wallet = user.wallet
        balance = float(grandtotal)-float(wallet)

        current_datetime = datetime.datetime.now()
        datetimenow = f"{current_datetime:%Y%m%d%H%M%S}"
        randomnumber = str(random.randint(11111, 99999))
        ordernumber = datetimenow+randomnumber

# for saving order
        if request.method == "POST":

            if usewallet:

                if user.wallet > grandtotal:
                    user.wallet = float(user.wallet) - float(grandtotal)
                    user.save()

                elif user.wallet < grandtotal:
                    user.wallet = 0
                    user.save()

            address = Address.objects.get(id=addressid)
            order = Order()
            order.user = user
            order.address = address
            order.order_number = ordernumber
            order.order_total = grandtotal
            order.wallet_amount = wallet
            order.deliverycharge = delivercharge
            order.save()

            if paymentmethod == 'cod':
                if balance == 0:
                    order.payment_method = 'WALLET'
                    order.payment_id = ordernumber+str(user.id)+'WALLET'
                else:
                    order.payment_method = 'COD'
                    order.payment_id = ordernumber+str(user.id)+'COD'

                order.save()
            else:
                if balance == 0:
                    order.payment_method = 'WALLET'
                    order.payment_id = ordernumber+str(user.id)+'WALLET'

                else:
                    paymentid = request.POST.get('payment_id')
                    order.payment_id = paymentid+str(user.id)+'UPI'
                    order.payment_method = 'UPI'

                order.save()
            # for order items
            for i in items:
                orderitems = OrderItems()
                productvarient = ProductVarient.objects.get(id=i.product.id)
                if productvarient.quantity > 0:
                    orderitems.order = order
                    orderitems.product = productvarient
                    orderitems.quantity = i.quantity
                    orderitems.unitprice = productvarient.product.discountprice
                    orderitems.product_price = productvarient.product.discountprice*i.quantity
                    orderitems.profit = (float(productvarient.product.discountprice)-float(
                        productvarient.product.costoftheproduct))*i.quantity
                    orderitems.save()
                    productvarient.quantity -= i.quantity
                    productvarient.save()
                    i.delete()
            return redirect('success')
        context = {
            'items': items,
            "grandtotal": grandtotal,
            'paymentmethod': paymentmethod,
            'wallet': wallet,
            'delivercharge': delivercharge,
            'balance': balance
        }

        return render(request, 'order/confirm.html', context)
    else:
        return redirect('offers')


# for razorpay
@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def proceed_to_pay(request):
    address = request.session.get('order')
    usewallet = address['wallet']
    temp = request.user
    user = CustomUser.objects.get(username=temp)
    items = Cart.objects.filter(user=user)
    grandtotal = 0
    for i in items:
        if i.product.quantity > 0:
            grandtotal += i.totalprice()
    if grandtotal < 1000:
        grandtotal += 70

    if usewallet:
        grandtotal = float(grandtotal) - float(user.wallet)

    payable_amount = grandtotal
    return JsonResponse({
        'payable_amount': payable_amount,
    })


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def success(request):
    if 'order' in request.session:
        del request.session['placeorder']
        del request.session['order']
        return render(request, 'order/success.html')
    else:
        return redirect('offers')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def userordersdetails(request, id):
    order = Order.objects.get(id=id)
    items = OrderItems.objects.filter(order=order)
    today = timezone.now()
    balancetopay = float(order.order_total) - float(order.wallet_amount)
    if order.payment_method == 'UPI':
        balancetopay = 0.00
    context = {
        'items': items,
        'order': order,
        'balancetopay': balancetopay,
        'today': today,
    }

    return render(request, 'order/userorder.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def cancelorder(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        itemId = request.POST.get('itemId')

        item = OrderItems.objects.get(id=itemId)
        item.is_cancelled = True
        item.reason = reason
        item.save()

        product = ProductVarient.objects.get(id=item.product.id)
        product.quantity += item.quantity
        product.save()

        order = Order.objects.get(id=item.order.id)
        order.order_total = float(order.order_total) - \
            float(item.product_price)
        order.save()

        user = order.user

        walletused = order.wallet_amount
        odertotal = order.order_total

        if walletused > odertotal:
            user.wallet = float(user.wallet) + \
                (float(walletused)-float(odertotal))
            order.wallet_amount = float(
                walletused)-(float(walletused)-float(odertotal))
            user.save()
            order.save()
        elif order.payment_method == 'UPI':
            user.wallet = float(user.wallet) + float(item.product_price)
            user.save()

        orderitem = OrderItems.objects.filter(order=order, is_cancelled=False)
        itemcount = orderitem.count()

        delivrycharge = 0
        if order.deliverycharge > 0:
            delivrycharge = 70

        if itemcount == 0:
            user.wallet = float(user.wallet) + float(delivrycharge)
            user.save()
            order.deliverycharge = 0
            order.order_total = 0
            order.save()

        return JsonResponse({"is_valid": True})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def returnproduct(request):
    name = request.user.username
    user = CustomUser.objects.get(username=name)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        itemId = request.POST.get('itemId')

        item = OrderItems.objects.get(id=itemId)
        item.is_cancelled = True
        item.reason = reason
        item.save()

        product = ProductVarient.objects.get(id=item.product.id)
        product.quantity += item.quantity
        product.save()

        order = Order.objects.get(id=item.order.id)
        order.order_total = float(order.order_total) - \
            float(item.product_price)
        order.save()

        user = order.user
        user.wallet = float(user.wallet) + float(item.product_price)
        user.save()

        delivrycharge = 0
        if order.deliverycharge > 0:
            delivrycharge = 70

        orderitem = OrderItems.objects.filter(order=order, is_cancelled=False)
        itemcount = orderitem.count()
        if itemcount == 0:
            user.wallet = float(user.wallet) + float(delivrycharge)
            user.save()
            order.deliverycharge = 0
            order.order_total = 0
            order.save()

        return JsonResponse({"is_valid": True})


# admin order
@login_required(login_url='adminlogin')
@cache_control(no_cache=True, no_store=True)
def orders(request):
    if 'admin' in request.session:
        # order = Order.objects.all()
        items = Order.objects.all()
        context = {
            'items': items
        }
        return render(request, 'order/aorder.html', context)
    else:
        return redirect('adminlogin')


@login_required(login_url='adminlogin')
@cache_control(no_cache=True, no_store=True)
def ordersdetails(request, id):
    if 'admin' in request.session:
        order = Order.objects.get(id=id)
        items = OrderItems.objects.filter(order=order)
        balancetopay = float(order.order_total) - float(order.wallet_amount)
        if order.payment_method == 'UPI':
            balancetopay = 0.00
        context = {
            'items': items,
            'order': order,
            'balancetopay': balancetopay
        }
        return render(request, 'order/aorderdetails.html', context)
    else:
        return redirect('adminlogin')


@login_required(login_url='adminlogin')
@cache_control(no_cache=True, no_store=True)
def orderstatus(request):
    if 'admin' in request.session:
        id = request.POST.get('orderId')
        print(id)
        status = request.POST.get('status')
        item = OrderItems.objects.get(id=id)
        item.status = status
        item.save()
        if status == 'Delivered':
            item.returndate = timezone.now()+timedelta(days=1)
            item.save()
        return JsonResponse({'is_valid': True})
    else:
        return redirect('adminlogin')
