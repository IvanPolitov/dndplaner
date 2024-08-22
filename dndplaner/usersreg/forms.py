from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))


class CustomUserCreationForm(UserCreationForm):
    usable_password = None

    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Password', max_length=30, widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='Confirm Password', max_length=30, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username',  'first_name', 'last_name',
                  'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
