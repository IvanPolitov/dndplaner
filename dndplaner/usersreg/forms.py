from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    usable_password = None

    # username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    # first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    # last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    # email = forms.EmailField(label='Email', widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    # password1 = forms.CharField(
    #     label='Password', max_length=30, widget=forms.PasswordInput(
    #         attrs={'class': 'form-control'}))
    # password2 = forms.CharField(
    #     label='Confirm Password', max_length=30, widget=forms.PasswordInput(
    #         attrs={'class': 'form-control'}))

    # class Meta:
    #     model = get_user_model()
    #     fields = ('username',  'first_name', 'last_name',
    #               'email', 'password1', 'password2')

    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Такой E-mail уже существует!")
    #     return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
