from django import forms
from django.contrib.auth.models import User
from .models import CartModel


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', help_text='The username must be unique and contain no spaces',
                               max_length=50)
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.CharField(label='Email', max_length=50, widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)


class ResetForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    username = forms.CharField(label='Username', max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email')


class PasswordChangeForm(forms.ModelForm):
    new_password_1 = forms.CharField(label='Enter a new password', widget=forms.PasswordInput)
    new_password_2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('new_password_1', 'new_password_2')


class AccountDelForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password',)


class CartForm(forms.ModelForm):
    pass
    # address = forms.CharField(label='Delivery address', max_length=115)
    # consent_processing = forms.NullBooleanField(label='Consent to data processing')
    # quantity_plorts = forms.RadioSelect()
    # date_delivery = forms.DateField(label='Date delivery')
    # date_order = forms.SplitHiddenDateTimeWidget()

    class Meta:
        pass
        # model = CartModel
        # fields = ('address', 'consent_processing', 'quantity_plorts', 'date_delivery', 'date_order')
