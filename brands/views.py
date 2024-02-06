from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from brands.models import Brands
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def brands(request):
    brands = Brands.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name').lower()
        image = request.FILES.get('image')
        description = request.POST.get('description')
        if Brands.objects.filter(name=name).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'Brand Name already Exist'})
        else:
            Brands.objects.create(name=name, image=image,
                                  description=description)
            return JsonResponse({'is_valid': True, 'error_message': 'Brand added Successfully'})

    context = {'brands': brands}
    return render(request, 'brands/brands.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def getbrands(request, id):
    temp = Brands.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('editname').lower()
        image = request.FILES.get('editimage')
        description = request.POST.get('editdescription')
        if Brands.objects.filter(name=name).exclude(id=id).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'Brand Name already Exist'})

        temp.name = name
        temp.description = description
        if image:
            if temp.image:
                old_image_path = temp.image.path
                default_storage.delete(old_image_path)
            temp.image = image
        temp.save()
        return JsonResponse({'is_valid': True, 'error_message': 'Brand details has updated'})
    brand_data = {
        'name': temp.name,
        'image': temp.image.url,
        'description': temp.description,
    }
    print('hi')
    return JsonResponse({"is_valid": True, "brand": brand_data})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def blockbrands(request, id):
    brand = Brands.objects.get(id=id)
    if brand.status:
        brand.status = False
    else:
        brand.status = True
    brand.save()
    return JsonResponse({"success": True})
