from django import forms
from django.contrib.auth.models import User
from .models import Cart, Purchase, Comments


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', help_text='The username must be unique and contain no spaces',
                               max_length=50)
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.CharField(label='Email', max_length=50, widget=forms.EmailInput)
    ConsentDataProcessing = forms.NullBooleanField(label='Consent to data processing')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'ConsentDataProcessing', 'password')


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


class AccountDelForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ('email',)


class CartForm(forms.ModelForm):
    deliveryAddress = forms.CharField(label='Delivery address', max_length=115)
    ConsentDataProcessing = forms.NullBooleanField(label='Consent to data processing')
    cartQuantity = forms.RadioSelect()
    dateDelivery = forms.DateField(label='Date delivery')

    class Meta:
        model = Cart
        fields = ('deliveryAddress', 'ConsentDataProcessing', 'cartQuantity', 'dateDelivery')


class PurchaseForm(forms.ModelForm):
    boughtQuantity = forms.RadioSelect()
    deliveryAddress = forms.CharField(max_length=115, label='Delivery address')
    dateDelivery = forms.DateField(label='Date delivery')

    class Meta:
        model = Purchase
        fields = ('boughtQuantity', 'deliveryAddress', 'dateDelivery')


class CommentsForm(forms.ModelForm):
    UserText = forms.CharField(max_length=1024, label='Comment', widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('UserText',)
