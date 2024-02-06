from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from product.models import Products
from wishlist.models import Wishlist
from security.models import CustomUser
# Create your views here.


@login_required(login_url='signin')
def wishlist(request):

    if request.user.is_authenticated and not request.user.is_superuser:

        temp = request.user
        user = CustomUser.objects.get(username=temp)
        products = Wishlist.objects.filter(user=user)
        context = {
            'products': products
        }

        return render(request, 'wishlist/wishlist.html', context)
    else:
        return redirect('signin')


@login_required(login_url='signin')
def addtowishlist(request):
    id = request.GET.get('product_id')
    temp = request.user
    user = CustomUser.objects.get(username=temp)
    products = Products.objects.get(id=id)
    item = Wishlist.objects.filter(user=user, product=products).first()
    if item:
        item.delete()
        return JsonResponse({'is_valid': False})

    Wishlist.objects.create(user=user, product=products)
    return JsonResponse({'is_valid': True})


@login_required(login_url='signin')
def rmwishlist(request):
    id = request.GET.get('wishlist_id')
    Wishlist.objects.get(id=id).delete()
    return JsonResponse({'is_valid': True})
