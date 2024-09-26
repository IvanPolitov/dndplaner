from typing import Any
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from .models import Room


def main(request):
    context = {
        'view_name': 'main',
    }
    return render(request, 'planer/main.html', context=context)


class RoomDetailView(DetailView):
    model = Room
    template_name = "planer/room.html"
    context_object_name = 'room'
    slug_url_kwarg = 'room_slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, quearyset=None, *args, **kwargs):
        return get_object_or_404(Room, slug=self.kwargs[self.slug_url_kwarg])


def add_room(request):
    context = {
        'view_name': 'add_room',
    }
    return render(request, 'planer/add_room.html', context=context)


def list_room(request):
    context = {
        'view_name': 'list_room',
    }
    return render(request, 'planer/list_room.html', context=context)
