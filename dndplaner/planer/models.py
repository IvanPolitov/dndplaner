import json
from typing import Any, Collection
from django.db import models
from django.urls import reverse
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    master = models.ForeignKey(
        'usersreg.CustomUser', on_delete=models.CASCADE, default=1)
    players = models.ManyToManyField(
        'usersreg.CustomUser', related_name='players')
    date = models.DateTimeField(default='1924-01-01 00:00:00')

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slug})

    @classmethod
    def from_db(cls, db: str | None, field_names: Collection[str], values: Collection[Any]):
        c = super().from_db(db, field_names, values)
        if c.date.date() < datetime.now().date():
            c.delete()
            return
        return c




class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(
        'usersreg.CustomUser', on_delete=models.PROTECT)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
