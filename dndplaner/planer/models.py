from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    master = models.ForeignKey(
        'usersreg.CustomUser', on_delete=models.PROTECT, null=True)
    players = models.ManyToManyField(
        'usersreg.CustomUser', related_name='players')

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slug})
