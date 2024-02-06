from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils import timezone
from datetime import datetime

from order.models import Order, OrderItems
# Create your views here.


@cache_control(no_cache=True, no_store=True)
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if '@' in username:
            username = User.objects.get(email=username).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                request.session['admin'] = True
                return JsonResponse({'is_valid': True})
            else:
                return JsonResponse({'is_valid': False, 'error_message': 'Username or password invalid'})

        else:
            return JsonResponse({'is_valid': False, 'error_message': 'Username or password invalid'})

    return render(request, 'admin/admin.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def dashboard(request):
    if 'admin' in request.session:
        orderitems = OrderItems.objects.filter(
            status='Delivered', is_cancelled=False)
        # ,returndate__lt=timezone.now()
        totalsalecount = orderitems.count()
        profit = 0
        totalsale = 0
        cod = 0
        wallet = 0
        upi = 0
        if orderitems:
            for i in orderitems:
                profit = float(profit)+float(i.profit)
                totalsale = float(totalsale)+float(i.product_price)
                if i.order.payment_method == 'COD':
                    cod += 1
                elif i.order.payment_method == 'UPI':
                    upi += 1
                else:
                    wallet += 1
            cod = round((cod/totalsalecount)*100)
            upi = round((upi/totalsalecount)*100)
            wallet = round((wallet/totalsalecount)*100)
        context = {
            'totalsalecount': totalsalecount,
            'profit': profit,
            'totalsale': totalsale,
            "cod": cod,
            'wallet': wallet,
            'upi': upi,
            'orderitems': orderitems,

        }
        if request.method == "POST":
            one = request.POST.get('one')
            two = request.POST.get('two')
            three = request.POST.get('three')
            print(one)
            if one:
                desired_date = datetime.strptime(one, '%Y-%m-%d').date()
                orderitems = OrderItems.objects.filter(
                    status='Delivered', is_cancelled=False, created_at__date=desired_date)
            else:
                two_date = datetime.strptime(two, '%Y-%m-%d')
                three_date = datetime.strptime(three, '%Y-%m-%d')
                orderitems = OrderItems.objects.filter(
                    status='Delivered', is_cancelled=False,  created_at__range=(two_date, three_date))
                if not orderitems:
                    orderitems = OrderItems.objects.filter(
                        status='Delivered', is_cancelled=False,  created_at__range=(three_date, two_date))

            profit1 = 0
            totalsale1 = 0
            if orderitems:
                for i in orderitems:
                    profit1 = float(profit1)+float(i.profit)
                    totalsale1 = float(totalsale1)+float(i.product_price)
            context['orderitems'] = orderitems
            context['one'] = one
            context['two'] = two
            context['three'] = three
            context['count'] = orderitems.count()
            context['profit1'] = profit1
            context['totalsale1'] = totalsale1
            return render(request, 'admin/dashboard.html', context)

        return render(request, 'admin/dashboard.html', context)
    else:
        return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def admindetails(request):
    return render(request, 'admin/admin details.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def adminsignout(request):
    request.session.flush()
    logout(request)
    return redirect('adminlogin')
