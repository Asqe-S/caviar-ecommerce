from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from coupons.models import Coupons
# Create your views here.


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def coupons(request):
    if request.method == "POST":
        couponcode = request.POST.get('code')
        validfrom = request.POST.get('from')
        expirydate = request.POST.get('expirydate')
        minimumorderamount = request.POST.get('purchase')
        percentage = request.POST.get('percentage')
        amount = request.POST.get('amount')
        if validfrom > expirydate:
            return JsonResponse({'is_valid': False, 'error_message': 'Please select valid expiry date'})
        if not percentage and not amount:
            return JsonResponse({'is_valid': False, 'error_message': 'Please enter offer Percentage or Rupees'})
        coupon = Coupons.objects.create(couponcode=couponcode.upper(), validfrom=validfrom,
                                        expirydate=expirydate, minimumorderamount=minimumorderamount)
        if percentage:
            coupon.off = percentage
        else:
            coupon.amount = amount
        coupon.save()
        return JsonResponse({'is_valid': True})
    coupon = Coupons.objects.all()
    context = {
        'coupon': coupon
    }
    return render(request, 'coupons/coupons.html', context)


def deletecoupons(request):
    id = request.GET.get('coupon_id')
    Coupons.objects.get(id=id).delete()
    return JsonResponse({'success': True})
