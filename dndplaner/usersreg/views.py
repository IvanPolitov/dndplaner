from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomUserAuthenticationForm


def user_login(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('main_window')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = CustomUserAuthenticationForm

    context = {
        'form': form,
    }

    return render(request, 'usersreg/login.html', context=context)


def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You are now registered')
            return redirect('main_window')
        else:
            messages.error(request, 'Invalid')
    else:
        form = CustomUserCreationForm

    context = {
        'form': form,
    }
    return render(request, 'usersreg/register.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('main_window')
