from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.crypto import get_random_string
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.contrib.auth.models import User
from security.models import CustomUser
from security.validation import *


# Create your views here.


# login
@cache_control(no_cache=True, no_store=True)
def signin(request):
    if request.user.is_superuser:
        return redirect('dashboard')
         
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('userdetails')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if '@' in username:
            tempuser = CustomUser.objects.filter(email=username).first()
            if tempuser:
                username = tempuser.username
            else:
                return JsonResponse({'is_valid': False, 'error_message': 'Email id is not valid'})
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_superuser:
            temp = CustomUser.objects.get(username=username)
            status = temp.status
            verified = temp.verified
            if not status:
                return JsonResponse({'is_valid': False, 'error_message': 'User was Blocked'})
            if not status:
                return JsonResponse({'is_valid': False, 'error_message': 'User was Blocked'})
            else:
                login(request, user)
                return JsonResponse({'is_valid': True})
        else:
            return JsonResponse({'is_valid': False, 'error_message': 'Username or password error'})
    return render(request, 'security/signin.html')


@login_required(login_url='signin')
@cache_control(no_cache=True, no_store=True)
def signout(request):
    request.session.flush()
    logout(request)
    return redirect('signin')


# create
@cache_control(no_cache=True, no_store=True)
def signup(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('userdetails')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        validusername = username_validator(username)
        validemail = email_validator(email)
        validphonenumber = phone_number_validator(phonenumber)
        validpassword = password_validator(password)

        if not validusername:
            return JsonResponse({'is_valid': False, 'error_message': 'not a valid username'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'username is already taken'})

        if not validemail:
            return JsonResponse({'is_valid': False, 'error_message': 'not a valid email'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'is_valid': False, 'error_message': 'email is already registered'})

        if not validphonenumber:
            return JsonResponse({'is_valid': False, 'error_message': 'not a valid valid phonenumber'})

        if not validpassword:
            return JsonResponse({'is_valid': False, 'error_message': 'password must be alphanumeric with symbols'})

        if password != confirmpassword:
            return JsonResponse({'is_valid': False, 'error_message': 'password missmatch'})

        otp = get_random_string(length=6, allowed_chars='9876543210')
        context = {
            'username': username,
            'email': email,
            'phonenumber': phonenumber,
            'password': password,
            'otp': otp
        }
        request.session['signup_complete'] = context
        subject = 'caviar account verification mail'
        emailcontext = {
            'username': username, 'otp': otp

        }
        message = render_to_string(
            'security/email.html', emailcontext)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.send()

        return JsonResponse({'is_valid': True})

    return render(request, 'security/signup.html')


@cache_control(no_cache=True, no_store=True)
def otp(request):

    if 'signup_complete' in request.session:
        user = request.session.get('signup_complete')
        username = user['username']
        email = user['email']
        phonenumber = user['phonenumber']
        password = user['password']
        otp = user['otp']
        if request.method == 'POST':
            userotp = request.POST.get('otp')
            if userotp == otp:
                user = CustomUser.objects.create_user(
                    username=username, email=email, phone_number=phonenumber, password=password)

                user.verified = True
                user.save()
                del request.session['signup_complete']
                return JsonResponse({'is_valid': True})
            else:

                return JsonResponse({'is_valid': False, 'error_message': 'not a valid otp'})

        return render(request, 'security/otp.html')
    elif 'forget' in request.session:
        recovery = request.session.get('forget')
        recoveryotp = recovery['otp']
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if otp == recoveryotp:
                return JsonResponse({'is_valid': 'recovery'})
            else:
                return JsonResponse({'is_valid': False, 'error_message': 'not a valid otp'})

        return render(request, 'security/otp.html')

    else:
        return redirect('signup')


@cache_control(no_cache=True, no_store=True)
def forgotpassword(request):
    if 'forget' in request.session:
        temp = request.session.get('forget')
        id = temp['user']
        user = CustomUser.objects.get(id=id)
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('userdetails')
        if request.method == "POST":
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            validpassword = password_validator(password)
            if not validpassword:
                return JsonResponse({'is_valid': False, 'error_message': 'password must be alphanumeric with symbols'})

            if password != confirmpassword:
                return JsonResponse({'is_valid': False, 'error_message': 'password missmatch'})
            user.set_password(password)
            user.save()
            del request.session['forget']
            return JsonResponse({'is_valid': True})

        return render(request, 'security/forgotpassword.html')
    else:
        return redirect('signin')


def femail(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('userdetails')
    if request.method == 'POST':
        tempuser = ''
        email = request.POST.get('username')

        if '@' not in email:
            tempuser = CustomUser.objects.filter(username=email).first()
            if tempuser:
                email = tempuser.email
            else:
                return JsonResponse({'is_valid': False, 'error_message': 'user not found'})
        else:
            tempuser = CustomUser.objects.filter(email=email).first()
            if not tempuser:
                return JsonResponse({'is_valid': False, 'error_message': 'user with email not found'})
        otp = get_random_string(length=6, allowed_chars='9876543210')
        context = {
            'otp': otp,
            'user': tempuser.id
        }
        request.session['forget'] = context
        subject = 'caviar account password recovery'
        emailcontext = {
            'username': tempuser.username, 'otp': otp, 'recovery': True

        }
        message = render_to_string(
            'security/email.html', emailcontext)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.send()

        return JsonResponse({'is_valid': True})

    return render(request, 'security/femail.html')
