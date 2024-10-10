from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime


from .models import Room, Message


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

    def clean_name(self):
        real_name = self.cleaned_data['name']
        name = set(self.cleaned_data['name'].lower())
        rus = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        eng = 'abcdefghijklmnopqrstuvwxyz'
        num = '0123456789'
        marks = ',_ -.?!:'

        name.difference_update(set(rus + eng + num + marks))
        if name:
            raise ValidationError(
                "В названии можно использовать только буквы русского и английского алфавита, цифры и знаки ,_ -.?!:")
        return real_name

    def clean_date(self):
        real_date = self.cleaned_data['date']

        if real_date.date() < datetime.now().date():
            raise ValidationError(
                "Дата не может быть в прошлом!")
        return real_date


class EnterRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ()


class DeleteRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ()


class MessageForm(forms.ModelForm):
    prefix = 'message'

    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),

        }
