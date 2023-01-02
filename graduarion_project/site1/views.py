import token

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
# from management.commands.from_emails import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, FORM_EMAIL
from django.core.mail import send_mail, mail_admins, EmailMessage
from .forms import RegistrationForm, LoginForm, ResetForm, PasswordChangeForm, AccountDelForm
from .models import Plorts
from django.conf import settings, global_settings
from django.views.generic import DeleteView, UpdateView

"""
Errors
"""


def m404(request):
    return HttpResponseNotFound('<h1>Not Found</h1>')


def error_frame_view(request):
    context = {

    }
    return render(request, 'errors/error_frame.html', context)


def error_frame_registration_view(request):
    context = {

    }
    return render(request, 'errors/error_frame_registration.html', context)


"""
Base view
"""


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


"""
Password reset view
"""


def password_reset_email_view(request):
    context = {

    }
    return render(request, 'errors/error_frame_registration.html', context)


def password_reset_view(request):
    # try:
    if request.method == "POST":
        user_form = ResetForm(data=request.POST)
        coun_users = 1
        user_chek = user_form.data.get  # сокращение для более удобного ввода в сравнение
        for i in User.objects.values('id', 'email', 'username', 'first_name', 'password', 'last_login'):
            # сравнение email и username отправленные пользователем с базой
            if user_chek('email') == i.get('email') and user_chek('username') == i.get('username'):

                send_mail(subject='Reset password', message=r"http://127.0.0.1:8000/account/password_reset/"
                                                            r"password_reset_done/password_reset_confirm/",
                          from_email=settings.FORM_EMAIL, auth_user=settings.EMAIL_HOST_USER,
                          auth_password=settings.EMAIL_HOST_PASSWORD, recipient_list=[i.get('email')],
                          fail_silently=False)
                # print(i.get('last_login'), i.get('email'), i.get('id'), i.get('password'))
                # token_new_passw = PasswordResetTokenGenerator().make_token(user=i)
                # send_mail(subject='Reset password', message=f"Hello, {i.get('first_name')}. \n"
                #                                             f"You can reset your password using this link: "
                #                                             f"{token_new_passw}",
                #           from_email=settings.FORM_EMAIL, auth_user=settings.EMAIL_HOST_USER,
                #           auth_password=settings.EMAIL_HOST_PASSWORD, recipient_list=[i.get('email')],
                #           fail_silently=False)

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
    # except:
    #     return redirect('error_frame')


def password_reset_done_view(request):
    try:
        context = {

        }
        return render(request, 'accounts/password_reset/password_reset_done.html', context)
    except:
        return redirect('error_frame')


def password_reset_confirm_view(request):
    try:
        if request.method == "POST":
            user_form = ResetForm(data=request.POST)
            if user_form.data.get('new_password_1') == user_form.data.get('new_password_2'):
                return redirect('password_reset_complete')
        context = {
            'form': PasswordChangeForm(),
        }
        return render(request, 'accounts/password_reset/password_reset_confirm.html', context)
    except:
        return redirect('error_frame')


def password_reset_complete_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/password_reset/password_reset_complete.html', context)
    except:
        return redirect('error_frame')


"""
Registration, login, logout
"""


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


"""
Delete account
"""


def delete_account_view(request):
    # try:
        if request.method == "POST":
            user_form = AccountDelForm(data=request.POST)
            user = DeleteView(password=user_form.data.get('password'))
            user_base = User.objects.values('id', 'username', 'password', 'email')
            # for i in User.objects.values('id', 'email', 'username', 'first_name', 'password', 'last_login'):
            #     # сравнение email и username отправленные пользователем с базой
            #     if user_chek('email') == i.get('email') and user_chek('username') == i.get('username'):
            #         send_mail(subject='Reset password', message=r"http://127.0.0.1:8000/account/password_reset/"
            #                                                     r"password_reset_done/password_reset_confirm/"
            #                                                     r"password_reset_email/",
            #                   from_email=settings.FORM_EMAIL, auth_user=settings.EMAIL_HOST_USER,
            #                   auth_password=settings.EMAIL_HOST_PASSWORD, recipient_list=[i.get('email')],
            #                   fail_silently=False)
            return redirect('delete_account_done')
        context = {
            'form': AccountDelForm(),
        }
        return render(request, 'accounts/delete_account/delete_account.html', context)
    # except:
    #     return redirect('error_frame')


def delete_account_done_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/delete_account/delete_account_done.html', context)
    except:
        return redirect('error_frame')