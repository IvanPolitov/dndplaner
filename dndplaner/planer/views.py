from django.forms import BaseModelForm
from django.forms.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Room
from .forms import RoomForm


def main(request):
    context = {
        'view_name': 'main',
    }
    return render(request, 'planer/main.html', context=context)


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya', ' ': '_'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class RoomDetailView(DetailView, FormMixin):
    model = Room
    form_class = None
    template_name = "planer/room.html"
    context_object_name = 'room'
    slug_url_kwarg = 'room_slug'

    def get_form(self, form_class: type | None = ...) -> BaseForm:
        return None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, quearyset=None, *args, **kwargs):
        return get_object_or_404(Room, slug=self.kwargs[self.slug_url_kwarg])

    def post(self, request, *args, **kwargs):
        print(request.POST)
        room = self.get_object()
        room.players.add(self.request.user)
        room.save()
        return self.get(request, *args, **kwargs)


class AddRoomView(CreateView):
    form_class = RoomForm
    template_name = 'planer/add_room.html'
    success_url = reverse_lazy('list_room')

    def form_valid(self, form):
        form.cleaned_data['slug'] = translit_to_eng(form.cleaned_data['name'])
        form.cleaned_data['master'] = self.request.user
        slug_in_db = Room.objects.filter(slug=form.cleaned_data['slug'])
        if slug_in_db:
            messages.error(self.request, 'Такого нет')
            return self.render_to_response(self.get_context_data(form=form))

        room = Room.objects.create(**form.cleaned_data)
        return redirect(room)


class RoomListView(ListView):
    model = Room
    template_name = 'planer/list_room.html'
    context_object_name = 'rooms'
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return super().get_queryset()
