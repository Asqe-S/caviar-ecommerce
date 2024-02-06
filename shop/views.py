from django.shortcuts import render
from django.views.decorators.cache import cache_control
from category.models import Category, Genders, SubCategory
from product.models import Products
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def offers(request):
    gender = Genders.objects.all()
    context = {
        'gender': gender

    }
    return render(request, 'shop/offers.html', context)


@cache_control(no_cache=True, no_store=True)
def shop(request, name, type):
    product = ''
    category = ''
    subcategory = ''
    if type == 'gender':
        bygender = Products.objects.filter(gender__name=name,
                                           active=True, brand__status=True, category__status=True, subcategory__status=True)

        category = Category.objects.filter(gender__name=name)
        product = bygender
        category = category

    if type == 'category':
        bycategory = Products.objects.filter(category__id=name,
                                             active=True, brand__status=True, category__status=True, subcategory__status=True)

        subcategory = SubCategory.objects.filter(category__id=name)
        product = bycategory
        subcategory = subcategory

    if type == 'subcategory':
        bysubcategory = Products.objects.filter(subcategory__id=name,
                                                active=True, brand__status=True, category__status=True, subcategory__status=True)
        product = bysubcategory

    if request.method == "POST":

        text = request.POST.get("search")
        bybrand = Products.objects.filter(brand__name__icontains=text,
                                          active=True, brand__status=True, category__status=True, subcategory__status=True)
        bygender = Products.objects.filter(gender__name__icontains=text,
                                           active=True, brand__status=True, category__status=True, subcategory__status=True)
        bycategory = Products.objects.filter(category__name__icontains=text,
                                             active=True, brand__status=True, category__status=True, subcategory__status=True)
        bysubcategory = Products.objects.filter(subcategory__name__icontains=text,
                                                active=True, brand__status=True, category__status=True, subcategory__status=True)
        byname = Products.objects.filter(name__icontains=text,
                                         active=True, brand__status=True, category__status=True, subcategory__status=True)
        product1 = ''
        if bygender:
            product1 = bygender
        if bycategory:
            product1 = bycategory
        if bysubcategory:
            product1 = bysubcategory
        if byname:
            product1 = byname
        if bybrand:
            product1 = bybrand

        context1 = {
            'product': product1,
        }
        return render(request, 'shop/shop.html', context1)

    paginator = Paginator(product, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'product': paged_products,
        'category': category,
        'subcategory': subcategory


    }
    return render(request, 'shop/shop.html', context)
