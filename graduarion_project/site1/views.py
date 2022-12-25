from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from utils.emails import SendingEmail
from .forms import RegistrationForm, LoginForm, ResetForm
from .models import Plorts


def shop_view(request):
    try:
        context = {
            'user': request.user,
            'plorts': Plorts.objects.all(),
        }
        return render(request, 'shop/shop.html', context)
    except:
        return redirect('error_frame')


def cart_view(request):
    try:
        context = {
            'plorts': Plorts.objects.all()
        }
        return render(request, 'cart/cart.html', context)
    except:
        return redirect('error_frame')


def error_frame_view(request):
    context = {

    }
    return render(request, 'shop/error_frame.html', context)


def password_reset_view(request):
    try:
        if request.method == "POST":
            user_form = ResetForm(data=request.POST)
            print(user_form.data)
            user = authenticate(email=user_form.data.get('email'))
            email_send = SendingEmail()
            email_send.sending_email(type_id=1, order=user)
            email_send.sending_email(type_id=2, email=user, order=user)
            return redirect('accounts/password_reset/password_reset_done.html')
        context = {
            'form': ResetForm(),
        }
        return render(request, 'accounts/password_reset/password_reset.html', context)
    except:
        return redirect('error_frame')


def password_reset_done_view(request):
    try:
        context = {

        }
        return render(request, 'accounts/password_reset/password_reset_done.html', context)
    except:
        return redirect('error_frame')


def registration_view(request):
    try:
        if request.method == 'POST':
            user_form = RegistrationForm(data=request.POST)
            if user_form.is_valid():
                User.objects.create_user(**user_form.cleaned_data)
                user = authenticate(username=user_form.cleaned_data.get('username'),
                                    name=user_form.cleaned_data.get('name'),
                                    last_name=user_form.cleaned_data.get('last_name'),
                                    email=user_form.cleaned_data.get('email'),
                                    password=user_form.cleaned_data.get('password'))
                print(user)
                login(request, user)
                return redirect('base')
            else:
                return redirect('error_frame')
        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'accounts/registration.html', context)
    except:
        return redirect('error_frame')


def login_view(request):
    try:
        if request.method == "POST":
            user_form = RegistrationForm(data=request.POST)
            print(user_form.data)
            user = authenticate(username=user_form.data.get('username'),
                                password=user_form.data.get('password'))
            login(request, user)
            return redirect('base')
        context = {
            'form': LoginForm(),
        }
        return render(request, 'accounts/account.html', context)
    except:
        return redirect('error_frame')


def logout_view(request):
    logout(request)
    return redirect('base')
