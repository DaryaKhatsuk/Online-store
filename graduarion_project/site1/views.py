from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm
from .models import Plorts


def shop_view(request):
    context = {
        'user': request.user,
        'plorts': Plorts.objects.all(),
    }
    return render(request, 'shop/shop.html', context)


def cart_view(request):
    context = {
        'plorts': Plorts.objects.all()
    }
    return render(request, 'cart/cart.html', context)


def registration_view(request):
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
            return HttpResponse('<h3>Данные не валидны!</h3>')
    context = {
        'form': RegistrationForm(),
    }
    return render(request, 'accounts/registration.html', context)


def login_view(request):
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


def logout_view(request):
    logout(request)
    return redirect('base')
