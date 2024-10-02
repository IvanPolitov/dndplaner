from django import forms
from django.contrib.auth import get_user_model

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'date']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'date': 'Дата игры',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(),
        }


class EnterRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ()
