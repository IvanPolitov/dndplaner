
from django.urls import path
from .views import *
from django.http import HttpResponse


urlpatterns = [
    path('', MainListView.as_view(), name='main_window'),
    path('rooms/<slug:room_slug>', RoomDetailView.as_view(), name='room'),
    path('add_room/', AddRoomView.as_view(), name='add_room'),
    path('rooms/', RoomListView.as_view(), name='list_room'),
    path('my_games/', MyGamesView.as_view(), name='my_games'),
    path('my_rooms/', MyRoomsView.as_view(), name='my_rooms'),
    path('test/', test, name='test'),
]
