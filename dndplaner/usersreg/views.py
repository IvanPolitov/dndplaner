from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomUserAuthenticationForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = CustomUserAuthenticationForm
    template_name = 'usersreg/login.html'
    extra_context = {'title': 'Login Login'}

    def get_success_url(self):
        return reverse_lazy('main_window')


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usersreg/register.html'
    extra_context = {'title': 'Register Register'}
    success_url = reverse_lazy('login')


def user_logout(request):
    logout(request)
    return redirect('main_window')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'usersreg/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self) -> str:
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "usersreg/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
