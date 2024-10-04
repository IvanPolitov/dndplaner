from django.db import models
from django.urls import reverse


class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    master = models.ForeignKey(
        'usersreg.CustomUser', on_delete=models.CASCADE)
    players = models.ManyToManyField(
        'usersreg.CustomUser', related_name='players')
    date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slug})


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(
        'usersreg.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
