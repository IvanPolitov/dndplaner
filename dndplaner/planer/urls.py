
from django.urls import path
from .views import *


urlpatterns = [
    path('', main, name='main_window'),
    path('room/<slug:room_slug>', RoomDetailView.as_view(), name='room'),
    path('add_room/', add_room, name='add_room'),
    path('list_room/', list_room, name='list_room'),
]
