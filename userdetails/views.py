from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from security.models import CustomUser
from security.validation import *
from django.contrib.auth import update_session_auth_hash
from userdetails.models import Address
from django.views.decorators.cache import cache_control
# Create your views here.


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def userdata(request):
    username = request.user.username
    user = CustomUser.objects.get(username=username)
    address = Address.objects.filter(user=user).order_by('id')
    context = {'address': address, 'tempuserid': user.id, 'user': user}
    return render(request, 'userdetails/details.html', context)


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def edituser(request, id):
    tempid = request.user.id

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        image = request.FILES.get('image')
        validusername = username_validator(username)
        validemail = email_validator(email)
        validphonenumber = phone_number_validator(phonenumber)
        if not validusername:
            return JsonResponse({'is_valid': False, 'error_message': 'not a valid username'})
        if User.objects.filter(username=username).exclude(id=tempid).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'username is already taken'})

        if not validemail:
            return JsonResponse({'is_valid': False, 'error_message': 'not a valid email'})
        if User.objects.filter(email=email).exclude(id=tempid).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'email is already registered'})

        if not validphonenumber:
            return JsonResponse({'is_valid': False, 'error_message': 'not a valid valid phonenumber'})
        tempuser = CustomUser.objects.get(id=id)

        tempuser.username = username
        tempuser.email = email
        tempuser.phone_number = phonenumber
        if image:
            if tempuser.image:
                old_image_path = tempuser.image.path
                default_storage.delete(old_image_path)
            tempuser.image = image

        tempuser.save()
        return JsonResponse({'is_valid': True, 'error_message': 'profile has updated'})

    return redirect('offers')


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def changepassword(request, id):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        validpassword = password_validator(password)
        print(password, confirmpassword)
        if not validpassword:
            print('hi')
            return JsonResponse({'is_valid': False, 'cperror_message': 'password must be alphanumeric with symbols'})

        if password != confirmpassword:
            return JsonResponse({'is_valid': False, 'cperror_message': 'password missmatch'})
        tempuser = CustomUser.objects.get(id=id)
        tempuser.set_password(password)
        tempuser.save()
        update_session_auth_hash(request, tempuser)
        print("Session authentication hash updated successfully.")  # Add this line

        return JsonResponse({'is_valid': True, 'cperror_message': 'profile has updated'})


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def addaddress(request):
    temp = request.user.username
    user = CustomUser.objects.get(username=temp)
    if request.method == 'POST':
        name = request.POST.get('name')
        type_of_address = request.POST.get('typeofaddress')
        phone_number = request.POST.get('phonenumber')
        alternate_phone_number = request.POST.get('alternatephonenumber')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        house = request.POST.get('houseaddress')
        road = request.POST.get('roadname')

        print(name, type_of_address, phone_number, user.email)
        Address.objects.create(
            user=user,
            name=name,
            type_of_address=type_of_address,
            phone_number=phone_number,
            alternate_phone_number=alternate_phone_number,
            pincode=pincode,
            city=city,
            state=state,
            house=house,
            road=road
        )
        return JsonResponse({'is_valid': True, 'error_message': 'Address Added'})
    else:
        return JsonResponse({'is_valid': False, 'error_message': 'Invalid request method'})


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def deleteaddress(request, id):
    Address.objects.get(id=id).delete()
    return JsonResponse({'is_valid': True, })


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def getaddress(request, id):
    address = Address.objects.get(id=id)
    address_data = {
        "name": address.name,
        "type_of_address": address.type_of_address,
        "phone_number": address.phone_number,
        "alternate_phone_number": address.alternate_phone_number,
        "pincode": address.pincode,
        "city": address.city,
        "state": address.state,
        "house": address.house,
        "road": address.road,
    }

    return JsonResponse({"is_valid": True, "address": address_data})


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def editaddress(request, id):
    address = Address.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST.get('editname')
        type_of_address = request.POST.get('edittypeofaddress')
        phone_number = request.POST.get('editphonenumber')
        alternate_phone_number = request.POST.get('editalternatephonenumber')
        pincode = request.POST.get('editpincode')
        city = request.POST.get('editcity')
        state = request.POST.get('editstate')
        house = request.POST.get('edithouseaddress')
        road = request.POST.get('editroadname')
        print(name, phone_number, alternate_phone_number)
        address.name = name
        address.type_of_address = type_of_address
        address.phone_number = phone_number
        address.alternate_phone_number = alternate_phone_number
        address.pincode = pincode
        address.city = city
        address.state = state
        address.house = house
        address.road = road
        address.save()
        print(address)
        return JsonResponse({'is_valid': True, 'error_message': 'Address Added'})
    else:
        return JsonResponse({'is_valid': False, 'error_message': 'Invalid request method'})


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def users(request):
    user = CustomUser.objects.all()
    context = {'user': user}
    return render(request, 'userdetails/user.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='adminlogin')
def blockusers(request, id):
    user = CustomUser.objects.get(id=id)
    if user.status:
        user.status = False
    else:
        user.status = True
    user.save()
    return JsonResponse({"success": True})
