
from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),

    path('logout/', user_logout, name='logout'),
    path('profile/', ProfileUser.as_view(), name='profile'),

    path('password-change/', UserPasswordChange.as_view(),
         name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name="usersreg/password_change_done.html"), name="password_change_done"),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name="usersreg/password_reset_form.html"),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name="usersreg/password_reset_done.html"),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="usersreg/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name="usersreg/password_reset_complete.html"), name='password_reset_complete'),
]
