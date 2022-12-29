from django import forms
from django.contrib.auth.models import User


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
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)


class ResetForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    username = forms.CharField(label='Username', max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email',)


class CartForm(forms.ModelForm):
    pass

    class Meta:
        pass
