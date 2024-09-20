from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomUserAuthenticationForm


class LoginUser(LoginView):
    form_class = CustomUserAuthenticationForm
    template_name = 'usersreg/login.html'
    extra_context = {'title': 'Login Login'}

    def get_success_url(self):
        return reverse_lazy('main_window')

# def user_login(request):
#     if request.method == 'POST':
#         form = CustomUserAuthenticationForm(data=request.POST)
#         if form.is_valid():
#             # строка ниже заменяет функцию аутентификации:
#             # def get_user(self):
#             #   return self.user_cache

#             # где self.user_cache =
#             #   authenticate(self.request, username = username, password = password)

#             user = form.get_user()

#             login(request, user)
#             messages.success(request, 'You are now logged in')
#             return redirect('main_window')
#         else:
#             messages.error(request, 'Invalid credentials')
#     else:
#         form = CustomUserAuthenticationForm()

#     context = {
#         'form': form,
#     }

#     return render(request, 'usersreg/login.html', context=context)


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usersreg/register.html'
    extra_context = {'title': 'Register Register'}
    success_url = reverse_lazy('main_window')

# def user_register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'You are now registered')
#             return redirect('main_window')
#         else:
#             messages.error(request, 'Invalid')
#     else:
#         form = CustomUserCreationForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'usersreg/register.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('main_window')
