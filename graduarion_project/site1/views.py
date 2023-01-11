from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User, make_password
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage, get_connection
from .forms import RegistrationForm, LoginForm, ResetForm, AccountDelForm, PurchaseForm, CommentsForm
from .models import Plorts, Purchase, Comments
from django.views.generic import DeleteView, UpdateView
from .helper_file import FORM_EMAIL, create
from django.contrib.sessions.middleware import SessionMiddleware, settings
from .forms import CartAddProductForm
from .cart import Cart


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

using session: request.session['foo'] = 'bar'    # задать переменную в сессии
               print(request.session.get('foo'))    # Извлечение session key
               del request.session['foo']    # Удалить key, хранящийся в session
"""


def shop_view(request):
    # try:
    #   del request.session['cart']
        cart_product_form = CartAddProductForm()
        context = {
            'user': request.user,
            'plorts': Plorts.objects.all(),
            'cart_product_form': cart_product_form,
        }
        return render(request, 'shop/shop.html', context)
    # except Exception as ex:
    #     print(ex)
    #     return redirect('error_frame')


def card_plort(request, num):
    # try:
        if request.method == 'POST':
            text_user = CommentsForm(data=request.POST)
            if text_user.is_valid():
                comment = Comments(idPlort=num,
                                   userName=request.user.first_name,
                                   idUser=request.user.id,
                                   UserText=text_user.data.get('UserText'))
                comment.save()
        cart_product_form = CartAddProductForm()
        context = {
            'plorts': Plorts.objects.filter(idPlort=num),
            'comments': Comments.objects.filter(idPlort=num),
            'comment_form': CommentsForm(),
            'product': num,
            'cart_product_form': cart_product_form,

        }
        return render(request, 'shop/card_plort.html', context)
    # except Exception as ex:
    #     print(ex)
    #     return redirect('error_frame')


@require_POST
def cart_add(request, product_id):
    print(product_id)
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    print(form)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(quantity=form.cleaned_data['quantity'],
                 product=product_id,
                 update_quantity=cd['update'],
                 )
    return redirect('base')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = product_id
    # print(product_id)
    # print(product)
    # print(cart.remove(product))
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    if request.method == 'POST':
        print(request.data.get())
        print(request.user())

        user = User.objects.get(id=request.user.id)
        # user.delete()
        # plorts = Plorts.objects.filter(idPlort=num)
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    context = {
        'cart_product_form': cart_product_form,
        'cart': cart,
        'form': PurchaseForm,
        'buy': Purchase,
    }
    return render(request, 'cart/cart.html', context)


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
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def password_reset_done_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/password_reset/password_reset_done.html', context)
    except Exception as ex:
        print(ex)
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
                        User.objects.create_user(username=user_form.cleaned_data.get('username'),
                                                 first_name=user_form.cleaned_data.get('first_name'),
                                                 last_name=user_form.cleaned_data.get('last_name'),
                                                 email=user_form.cleaned_data.get('email'),
                                                 password=user_form.cleaned_data.get('password'))
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
            # request.session['shop'] = 'buy'
            user_form = RegistrationForm(data=request.POST)
            user = authenticate(username=user_form.data.get('username'),
                                password=user_form.data.get('password'))
            login(request, user)
            # if request.session.is_empty():
            #     request.session['shop'] = 'buy'
            return redirect('base')
        context = {
            'form': LoginForm(),
        }
        return render(request, 'accounts/account.html', context)
    except Exception as ex:
        print(ex)
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
            user_form = AccountDelForm(data=request.POST)
            if user_form.is_valid() and user_form.data.get('email') == request.user.email:
                with get_connection() as connection:
                    EmailMessage(subject='Delete account', body=f"Dear {request.user.first_name}, your account on "
                                                                f"PlortShop.Zz as deleted.",
                                 from_email=FORM_EMAIL, to=[request.user.email], connection=connection).send()
                    user = User.objects.get(id=request.user.id)
                    user.delete()
                    return redirect('delete_account_done')
        context = {
            'form': AccountDelForm(),
        }
        return render(request, 'accounts/delete_account/delete_account.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def delete_account_done_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/delete_account/delete_account_done.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')
