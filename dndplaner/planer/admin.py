from django.contrib import admin
from .models import Room

# Register your models here.


class RoomAdmin(admin.ModelAdmin):

    model = Room
    list_display = ['name', 'master', 'date']


admin.site.register(Room)
