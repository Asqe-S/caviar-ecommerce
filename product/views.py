from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from brands.models import Brands
from category.models import Category, Genders, SubCategory
from order.models import OrderItems, Review
from product.models import MultipleImages, ProductVarient, Products,  Size
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.


@cache_control(no_cache=True, no_store=True)
def product(request, id):
    products = Products.objects.get(id=id)
    varient = ProductVarient.objects.filter(product=products)
    multipleimage = MultipleImages.objects.filter(product=products)
    review = Review.objects.filter(product=products)

    related = Products.objects.filter(category__id=products.category.id,
                                      active=True, brand__status=True, category__status=True, subcategory__status=True).exclude(id=id)[:3]

    context = {
        'products': products,
        'multipleimage': multipleimage,
        'varient': varient,
        'related': related,
        'review': review
    }
    return render(request, 'product/product.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def blockproduct(request):
    id = request.GET.get('productId')
    poduct = Products.objects.get(id=id)
    if poduct.active:
        poduct.active = False
    else:
        poduct.active = True
    poduct.save()
    return JsonResponse({"success": True})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def addproduct(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            costoftheproduct = request.POST.get('costoftheproduct')
            sellingprice = request.POST.get('sellingprice')
            discountprice = request.POST.get('discountprice')

            genderid = request.POST.get('gender')
            gender = Genders.objects.get(id=genderid)

            brandid = request.POST.get('brand')
            brand = Brands.objects.get(id=brandid)

            categoryid = request.POST.get('category')
            category = Category.objects.get(id=categoryid)

            subcategoryid = request.POST.get('subcategory')
            subcategory = SubCategory.objects.get(id=subcategoryid)

            image = request.FILES.get('image')
            product = Products.objects.create(
                name=name, description=description, costoftheproduct=costoftheproduct, sellingprice=sellingprice, discountprice=discountprice, gender=gender, brand=brand, category=category, subcategory=subcategory, image=image
            )
            multipleimage = request.FILES.getlist('multipleimage')
            for img in multipleimage:
                temp = MultipleImages.objects.create(product=product,
                                                     multipleimages=img)
                temp.save()

            return JsonResponse({'is_valid': True, 'message': 'product addded successfully'})
        gender = Genders.objects.all()
        brands = Brands.objects.filter(status='True')
        product = Products.objects.all()
        size = Size.objects.all()
        context = {
            'gender': gender,
            'brands': brands,
            'product': product,
            'size': size
        }
        return render(request, 'product/addproduct.html', context)
    else:
        return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def editproducts(request, id):
    if 'admin' in request.session:
        product = Products.objects.get(id=id)

        if request.method == 'POST':
            name = request.POST.get('editname')
            description = request.POST.get('editdescription')
            costoftheproduct = request.POST.get('costoftheproduct')
            sellingprice = request.POST.get('sellingprice')
            discountprice = request.POST.get('discountprice')

            genderid = request.POST.get('editgender')
            gender = Genders.objects.get(id=genderid)

            brandid = request.POST.get('editbrand')
            brand = Brands.objects.get(id=brandid)

            categoryid = request.POST.get('editcategory')
            category = Category.objects.get(id=categoryid)

            subcategoryid = request.POST.get('editsubcategory')
            subcategory = SubCategory.objects.get(id=subcategoryid)
            product.name = name
            product.description = description
            product.gender = gender
            product.brand = brand
            product.category = category
            product.subcategory = subcategory
            product.costoftheproduct = costoftheproduct
            product.sellingprice = sellingprice
            product.discountprice = discountprice

            image = request.FILES.get('editimage')
            if image:
                if product.image:
                    old_image_path = product.image.path
                    default_storage.delete(old_image_path)
                product.image = image

            product.save()

            multipleimage = request.FILES.getlist('editmultipleimage')
            if multipleimage:
                m_image = MultipleImages.objects.filter(product=product)
                for i in m_image:
                    default_storage.delete(i.multipleimages.path)
                    i.delete()

                for img in multipleimage:
                    temp = MultipleImages.objects.create(product=product,
                                                         multipleimages=img)
                    temp.save()
            return redirect('addproduct')
        brand = Brands.objects.all().exclude(id=product.brand.id)
        gender = Genders.objects.all().exclude(id=product.gender.id)
        category = Category.objects.filter(gender=product.gender)
        subcategory = SubCategory.objects.filter(category=product.category)

        context = {
            'product': product,
            'brands': brand,
            'gender': gender,
            'category': category,
            'subcategory': subcategory,

        }

        return render(request, 'product/editproduct.html', context)
    else:
        return redirect('adminlogin')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def addvarient(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')
        product = Products.objects.get(id=productId)

        sizeid = request.POST.get('size')
        size = Size.objects.get(id=sizeid)

        quantity = request.POST.get('quantity')

        if ProductVarient.objects.filter(product=product, size=size).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'varient aleady exist'})

        ProductVarient.objects.create(product=product, size=size, quantity=quantity,
                                      )
        product.active = True
        product.save()
    return JsonResponse({'is_valid': True, 'error_message': 'varient added'})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def editvarient(request, id):
    varient = ProductVarient.objects.get(id=id)

    if request.method == "POST":

        quantity = request.POST.get('equantity')
        varient.quantity = quantity
        varient.save()
        return JsonResponse({'is_valid': True, 'error_message': 'Vaient edited'})

    varient_data = {
        'quantity': varient.quantity,
    }

    return JsonResponse({'is_valid': True, 'varient': varient_data})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def getcategory(request):
    gender_id = request.GET.get('gender_id')
    categories = Category.objects.filter(gender_id=gender_id)

    category_options = [{'id': category.id, 'name': category.name}
                        for category in categories]

    data = {
        'categories': category_options,
    }

    return JsonResponse(data)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def getsubcategory(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    subcategory_options = [{'id': subcategory.id, 'name': subcategory.name}
                           for subcategory in subcategories]

    data = {
        'categories': subcategory_options,
    }

    return JsonResponse(data)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='signin')
def review(request):
    if request.method == "POST":
        review = request.POST.get('review')
        id = request.POST.get('itemId')
        orderitem = OrderItems.objects.get(id=id)
        product = Products.objects.get(id=orderitem.product.product.id)
        updatereview = Review.objects.filter(orderitems=orderitem)
        if updatereview:
            updatereview[0].review = review
            updatereview[0].save()
        else:
            Review.objects.create(
                user=request.user, product=product, review=review, orderitems=orderitem)
    return JsonResponse({'is_valid': True})
