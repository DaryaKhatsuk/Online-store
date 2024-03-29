from django import forms
from django.contrib.auth.models import User
from .models import Purchase, Comments, Support


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', help_text='The username must be unique and contain no spaces',
                               max_length=50)
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.CharField(label='Email', max_length=50, widget=forms.EmailInput,
                            help_text='Please use a valid email address so that you can be contacted')
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


class PurchaseForm(forms.ModelForm):
    deliveryAddress = forms.CharField(max_length=115, label='Delivery address')
    dateDelivery = forms.DateField(label='Date delivery', widget=forms.SelectDateWidget)

    class Meta:
        model = Purchase
        fields = ('deliveryAddress', 'dateDelivery')


class CommentsForm(forms.ModelForm):
    UserText = forms.CharField(max_length=1024, label='Comment', widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('UserText',)


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class SupportForm(forms.ModelForm):
    UserText = forms.CharField(max_length=2000, label='Message', widget=forms.Textarea)
    emailUser = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput)

    class Meta:
        model = Support
        fields = ('UserText', 'emailUser')
