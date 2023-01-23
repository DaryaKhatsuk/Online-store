from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage, get_connection, mail_admins
from .forms import RegistrationForm, LoginForm, ResetForm, AccountDelForm, PurchaseForm, CommentsForm, SupportForm
from .models import Plorts, Purchase, Comments, Support
from .helper_file import FORM_EMAIL, create, EMAIL_ADMIN
from .forms import CartAddProductForm
from .cart import Cart
from datetime import date, datetime

"""
Errors
"""


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
    try:
        if len(Plorts.objects.all()) > 1:
            cart_product_form = CartAddProductForm()
            context = {
                'user': request.user,
                'plorts': Plorts.objects.all(),
                'cart_product_form': cart_product_form,
            }
            return render(request, 'shop/shop.html', context)
        else:
            commad_start = Command()
            commad_start.handle()
            cart_product_form = CartAddProductForm()
            context = {
                'user': request.user,
                'plorts': Plorts.objects.all(),
                'cart_product_form': cart_product_form,
            }
            return render(request, 'shop/shop.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def card_plort(request, num):
    try:
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
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Support
"""


def support_view(request):
    try:
        if request.method == 'POST':
            support_form = SupportForm(data=request.POST)
            if support_form.is_valid():
                supportBase = Support(emailUser=support_form.data.get('emailUser'),
                                      UserText=support_form.data.get('UserText'),
                                      )
                supportBase.save()
                print(supportBase.idSupport)
                with get_connection() as connection:
                    EmailMessage(subject='Need support', body=f"Date: {date.today()}\n"
                                                              f"Email: {support_form.data.get('emailUser')}\n"
                                                              f"Message: {support_form.data.get('UserText')}",
                                 from_email=EMAIL_ADMIN, to=[EMAIL_ADMIN],
                                 connection=connection).send()
                    return redirect('support_done')
        context = {
            'form': SupportForm,
        }
        return render(request, 'support/support.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def support_done_view(request):
    try:
        context = {
        }
        return render(request, 'support/support_done.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


"""
Card view
"""


@require_POST
def cart_add(request, product_id):
    try:
        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(quantity=form.cleaned_data['quantity'],
                     product=product_id,
                     update_quantity=cd['update'],
                     )
        return redirect('base')
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def cart_remove(request, product_id):
    try:
        cart = Cart(request)
        product = product_id
        cart.remove(product)
        return redirect('cart_detail')
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def cart_detail(request):
    try:
        cart = Cart(request)
        cart_product_form = CartAddProductForm()
        if request.method == 'POST':
            purchaseform = PurchaseForm(data=request.POST)
            cart_product_form = CartAddProductForm(data=request.POST)
            if purchaseform.is_valid():
                purchaseform_date = datetime(int(purchaseform.data.get('dateDelivery_year')),
                                             int(purchaseform.data.get('dateDelivery_month')),
                                             int(purchaseform.data.get('dateDelivery_day'))).date()

                if purchaseform_date > date.today():
                    cart_session = request.session['cart']
                    coun_objects = 0
                    email_from_send = ''
                    for item, dataItem in cart_session.items():
                        changesPlorts = Plorts.objects.get(idPlort=item)
                        if changesPlorts.quantity - dataItem.get('quantity') >= 0:
                            changesPlorts.quantity -= dataItem.get('quantity')
                            totalPrice = int(dataItem.get('price')) * int(dataItem.get('quantity'))
                            buying = Purchase(boughtPlort=changesPlorts.idPlort,
                                              pricePlort=dataItem.get('price'),
                                              boughtQuantity=dataItem.get('quantity'),
                                              totalPrice=totalPrice,
                                              deliveryAddress=purchaseform.data.get('deliveryAddress'),
                                              dateDelivery=purchaseform_date,
                                              currentCustomer=request.user.id,
                                              )
                            buying.save()
                            changesPlorts.save()
                            email_from_send += f"Ordered №{buying.idPurchase}:\n" \
                                               f"Plort: {changesPlorts.plortName},\n" \
                                               f"Price: {dataItem.get('price')},\n" \
                                               f"Quantity: {dataItem.get('quantity')},\n" \
                                               f"Sum: {totalPrice}.\n"
                            coun_objects += 1
                        else:
                            return redirect('too_much_plorts')
                        if coun_objects == len(cart_session.items()):
                            with get_connection() as connection:
                                EmailMessage(subject='Your order from PlortShop.Zz',
                                             body=f"Dear {request.user.first_name},\n"
                                             f"thank you for your order. In case of any problems, we will contact you."
                                             f"\nOrder Details:\n{email_from_send}"
                                             f"Desired delivery date: {purchaseform_date}\n"
                                             f"The address: {purchaseform.data.get('deliveryAddress')}\n",
                                             from_email=FORM_EMAIL, to=[request.user.email],
                                             connection=connection).send()
                            with get_connection() as connection:
                                EmailMessage(subject='Order',
                                             body=f"The buyer under the nickname {request.user.username}\n"
                                                  f"Name: {request.user.first_name}\n"
                                                  f"Surname: {request.user.last_name}\n"
                                                  f"Order date: {buying.dateOrder}\n"
                                                  f"Desired delivery date: {purchaseform_date}\n"
                                                  f"The address: {purchaseform.data.get('deliveryAddress')}\n"
                                                  f"His email: {request.user.email}\n{email_from_send}",
                                             from_email=EMAIL_ADMIN, to=[EMAIL_ADMIN], connection=connection).send()

                            del request.session['cart']
                            return redirect('cart_done')
                elif purchaseform_date <= date.today():
                    return redirect('cart_not_done')

        context = {
            'cart_product_form': cart_product_form,
            'cart': cart,
            'form': PurchaseForm,
        }
        return render(request, 'cart/cart.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def cart_done(request):
    try:
        context = {
        }
        return render(request, 'cart/purchases_register.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def cart_not_done_view(request):
    try:
        context = {
        }
        return render(request, 'cart/order_not_appr.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


def much_plorts_view(request):
    try:
        context = {
        }
        return render(request, 'cart/too_much_plorts.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')


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
        plorts = {}
        if request.user.is_superuser == True:
            for idPurchase in Purchase.objects.values('idPurchase', 'boughtPlort', 'pricePlort', 'boughtQuantity',
                                                      'totalPrice', 'deliveryAddress', 'dateDelivery', 'dateOrder',
                                                      'currentCustomer'):
                plort = Plorts.objects.get(idPlort=idPurchase.get('boughtPlort'))
                user = User.objects.get(id=idPurchase.get('currentCustomer'))
                plorts[idPurchase.get('idPurchase')] = {'idPurchase': idPurchase.get('idPurchase'),
                                                        'pricePlort': idPurchase.get('pricePlort'),
                                                        'boughtQuantity': idPurchase.get('boughtQuantity'),
                                                        'totalPrice': idPurchase.get('totalPrice'),
                                                        'deliveryAddress': idPurchase.get('deliveryAddress'),
                                                        'dateOrder': idPurchase.get('dateOrder'),
                                                        'dateDelivery': idPurchase.get('dateDelivery'),
                                                        'boughtPlort': plort.plortName, 'username': user.username,
                                                        'first_name': user.first_name, 'last_name': user.last_name,
                                                        'email': user.email
                                                        }
        plorts_user = {}
        if not request.user.is_superuser:
            for purchases in Purchase.objects.values('idPurchase', 'boughtPlort', 'pricePlort', 'boughtQuantity',
                                                     'totalPrice', 'deliveryAddress', 'dateDelivery', 'dateOrder')\
                                                    .filter(currentCustomer=request.user.id):
                plort = Plorts.objects.get(idPlort=purchases.get('boughtPlort'))
                plorts_user[purchases.get('idPurchase')] = {'idPurchase': purchases.get('idPurchase'),
                                                            'pricePlort': purchases.get('pricePlort'),
                                                            'boughtQuantity': purchases.get('boughtQuantity'),
                                                            'totalPrice': purchases.get('totalPrice'),
                                                            'deliveryAddress': purchases.get('deliveryAddress'),
                                                            'dateOrder': purchases.get('dateOrder'),
                                                            'dateDelivery': purchases.get('dateDelivery'),
                                                            'boughtPlort': plort.plortName
                                                            }
        if request.method == "POST":
            user_form = RegistrationForm(data=request.POST)
            user = authenticate(username=user_form.data.get('username'),
                                password=user_form.data.get('password'))
            login(request, user)
            return redirect('base')
        context = {
            'user': request.user,
            'form': LoginForm(),
            'purchases': plorts_user.values(),
            'plorts': plorts.values(),
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
            if Purchase.objects.filter(currentCustomer=request.user.id):
                return redirect('not_delete')
            else:
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


def not_delete_view(request):
    try:
        context = {
        }
        return render(request, 'accounts/delete_account/not_delete.html', context)
    except Exception as ex:
        print(ex)
        return redirect('error_frame')
