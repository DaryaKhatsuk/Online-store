from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail, mail_admins, send_mass_mail, EmailMessage
from .forms import RegistrationForm, LoginForm, ResetForm
from .models import Plorts


def m404(request):
    return HttpResponseNotFound('<h1>Not Found</h1>')


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

        }
        return render(request, 'cart/cart.html', context)
    except:
        return redirect('error_frame')


def error_frame_view(request):
    context = {

    }
    return render(request, 'errors/error_frame.html', context)


def error_frame_registration_view(request):
    context = {

    }
    return render(request, 'errors/error_frame_registration.html', context)


def password_reset_view(request):
    try:
        if request.method == "POST":
            user_form = ResetForm(data=request.POST)
            coun_users = 1
            user_chek = user_form.data.get    # сокращение для более удобного ввода в сравнение
            for i in User.objects.values('email', 'username'):
                # сравнение email и username отправленные пользователем с базой
                if user_chek('email') == i.get('email') and user_chek('username') == i.get('username'):
                    return redirect('password_reset_done')
                # только если coun_users будет равно количеству записей в базе и до этого не найдется запись,
                # выходит экран ошибки
                elif coun_users == len(User.objects.all()):
                    return redirect('error_frame')
                coun_users += 1
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
                coun_users = 1

                for i in User.objects.values('email'):
                    # только если coun_users будет равно количеству записей в базе и до этого не найдется запись
                    # об искомом email, email будет зарегистрирован
                    if coun_users == len(User.objects.all()) and user_form.data.get('email') != i.get('email'):
                        User.objects.create_user(**user_form.cleaned_data)
                        user = authenticate(username=user_form.cleaned_data.get('username'),
                                            first_name=user_form.cleaned_data.get('first_name'),
                                            last_name=user_form.cleaned_data.get('last_name'),
                                            email=user_form.cleaned_data.get('email'),
                                            password=user_form.cleaned_data.get('password'))
                        login(request, user)
                        return redirect('base')
                    elif user_form.data.get('email') == i.get('email'):
                        return redirect('error_frame_registration')
                    coun_users += 1

        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'accounts/registration.html', context)
    except AttributeError as ae:
        print(ae)
        return redirect('error_frame_registration')
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def login_view(request):
    try:
        if request.method == "POST":
            user_form = RegistrationForm(data=request.POST)
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
