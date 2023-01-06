from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User, make_password
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, get_connection
from .forms import RegistrationForm, LoginForm, ResetForm, AccountDelForm
from .models import Plorts
from django.views.generic import DeleteView, UpdateView
from .helper_file import FORM_EMAIL, create

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


# def cart_view(request):
#     try:
#         context = {
#
#         }
#         return render(request, 'cart/cart.html', context)
#     except:
#         return redirect('error_frame')


"""
Password reset view
"""


def password_reset_view(request):
    try:
        if request.method == "POST":
            user_form = ResetForm(data=request.POST)
            coun_users = 1
            user_chek = user_form.data.get  # сокращение для более удобного ввода в сравнение
            for i in User.objects.values('id', 'email', 'username', 'first_name'):
                # сравнение email и username отправленные пользователем с базой
                if user_chek('email') == i.get('email') and user_chek('username') == i.get('username'):
                    with get_connection() as connection:
                        new_password = create()
                        EmailMessage(subject='Reset password', body=f"Dear {i.get('first_name')}!\n"
                                                                    f"Your new password: {new_password}\n"
                                                                    f"Please write it down and delete this message.",
                                     from_email=FORM_EMAIL, to=[i.get('email')], connection=connection).send()
                        set_user = User.objects.get(username=user_chek('username'))
                        set_user.set_password(new_password)
                        set_user.save()

                        print(f"Пользователь с id и username: {i.get('id'), user_chek('username')}, сменил пароль")

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
    try:
        if request.method == "POST":
            print(request.user.first_name)
            user_form = AccountDelForm(data=request.POST)
            user_base_id = User.objects.values('id', 'email')
            coun_users = 0
            for i in user_base_id:
                coun_users += 1
                if user_form.data.get('email') == i.get('email'):
                    with get_connection() as connection:
                        EmailMessage(subject='Delete account', body=f"Dear {request.user.first_name}, your account on "
                                                                    f"PlortShop.Zz as deleted.",
                                     from_email=FORM_EMAIL, to=[i.get('email')], connection=connection).send()
                        user = User.objects.get(id=i.get('id'))
                        user.delete()
                        return redirect('delete_account_done')
                elif coun_users == len(user_base_id):
                    return redirect('error_frame')
        context = {
            'form': AccountDelForm(),
        }
        return render(request, 'accounts/delete_account/delete_account.html', context)
    except:
        return redirect('error_frame')


def delete_account_done_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/delete_account/delete_account_done.html', context)
    except:
        return redirect('error_frame')
