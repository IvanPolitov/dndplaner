
from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('password-change/', UserPasswordChange.as_view(),
         name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name="usersreg/password_change_done.html"), name="password_change_done"),
]
