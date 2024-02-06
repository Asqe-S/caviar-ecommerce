from django.shortcuts import render, redirect
from cart.models import Cart
from product.models import ProductVarient
from security.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import cache_control

# Create your views here.


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def cart(request):
    temp = request.user
    user = CustomUser.objects.get(username=temp)
    items = Cart.objects.filter(user=user)
    grandtotal = 0
    totalitems = 0
    outofstock = False
    for i in items:
        if i.product.quantity > 0:
            totalitems += 1
        else:
            outofstock = True

    for i in items:
        grandtotal += float(i.totalprice())
    context = {
        'items': items,
        'grandtotal': grandtotal,
        'totalitems': totalitems,
        'outofstock': outofstock
    }
    request.session['placeorder'] = True
    return render(request, 'cart/cart.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def addtocart(request):
    temp = request.user
    user = CustomUser.objects.get(username=temp)

    if request.method == "POST":
        id = request.POST.get('size')
        quantity = request.POST.get('quantity')
        product = ProductVarient.objects.get(id=id)
        if int(quantity) > int(product.quantity):
            return JsonResponse({'is_valid': False, 'error_message': f'unavailabe stock'})
        cartitem = Cart.objects.filter(user=user, product=product).first()
        if cartitem:
            return JsonResponse({'is_valid': False, 'error_message': 'Item was already in the cart'})
        total = float(quantity) * float(product.product.discountprice)
        Cart.objects.create(user=user, product=product,
                            quantity=quantity, total=total)
        return JsonResponse({'is_valid': True, 'error_message': 'Item added to the cart'})

    return JsonResponse({'is_valid': True})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def removefromcart(request):
    id = request.GET.get('cartitem_id')
    Cart.objects.get(id=id).delete()
    return JsonResponse({'is_valid': True})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def addcartquantity(request):
    text = request.GET.get('count_val')
    id = request.GET.get('id')
    cartitem = Cart.objects.get(id=id)

    if text == '1':
        cartitem.quantity += 1
    else:
        cartitem.quantity -= 1
    cartitem.total = float(cartitem.quantity) * \
        float(cartitem.product.product.discountprice)
    cartitem.save()

    return JsonResponse({'is_valid': True})
