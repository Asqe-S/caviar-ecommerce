from django.shortcuts import render
from django.http import JsonResponse
from category.models import Category, Genders, SubCategory
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def category(request):
    if request.method == "POST":
        temp_gender = request.POST.get('gender')
        category = request.POST.get('category')
        gndr = Genders.objects.get(id=temp_gender)
        if Category.objects.filter(gender=gndr, name=category).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'category already exixts'})

        Category.objects.create(gender=gndr, name=category)
        return JsonResponse({'is_valid': True, 'error_message': 'category added'})
    gender = Genders.objects.all()
    context = {'genders': gender}
    return render(request, 'category/category.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def subcategory(request):
    if request.method == "POST":
        category = request.POST.get('category')
        sub = request.POST.get('subcategory')
        ctgry = Category.objects.get(id=category)
        SubCategory.objects.create(category=ctgry, name=sub)
        return JsonResponse({'is_valid': True, 'error_message': 'category added'})
