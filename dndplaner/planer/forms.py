from django import forms
from django.contrib.auth import get_user_model

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EnterRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ()
