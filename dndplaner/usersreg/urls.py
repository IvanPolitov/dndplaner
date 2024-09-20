
from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),

]
