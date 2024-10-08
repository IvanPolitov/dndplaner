import json
from .forms import RoomForm, EnterRoomForm, DeleteRoomForm, MessageForm
from .models import Room, Message
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, FormView
from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core import serializers


def test(request):
    return render(request, 'planer/test.html')


class MainListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'planer/main.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = Room.objects.filter(Q(players__id=self.request.user.id) | Q(
            master__id=self.request.user.id)).order_by('date')
        return queryset

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya', ' ': '_'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class RoomDetailView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = EnterRoomForm
    template_name = "planer/room.html"
    context_object_name = 'room'
    slug_url_kwarg = 'room_slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        message_form = MessageForm()
        comments = Message.objects.filter(
            room__slug=self.kwargs[self.slug_url_kwarg]).order_by('-timestamp')

        context['message'] = message_form
        context['comments'] = comments
        return context

    def get_object(self, quearyset=None, *args, **kwargs):
        return get_object_or_404(Room, slug=self.kwargs[self.slug_url_kwarg])

    def post(self, request, *args, **kwargs):
        room = self.get_object()
        if room.master == self.request.user:
            return redirect(room)

        if room.players.filter(id=self.request.user.id).exists():
            room.players.remove(self.request.user)
        else:
            room.players.add(self.request.user)
            room.save()
        return redirect(room)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any):
        q = super().get(request, *args, **kwargs)
        return q


class AddRoomView(LoginRequiredMixin, CreateView):
    form_class = RoomForm
    template_name = 'planer/add_room.html'
    success_url = reverse_lazy('list_room')

    def form_valid(self, form):
        form.cleaned_data['slug'] = translit_to_eng(form.cleaned_data['name'])
        form.cleaned_data['master'] = self.request.user
        slug_in_db = Room.objects.filter(slug=form.cleaned_data['slug'])
        if slug_in_db:

            messages.error(self.request, 'Комната с таким названием уже есть')
            return self.render_to_response(self.get_context_data(form=form))

        room = Room.objects.create(**form.cleaned_data)
        return redirect(room)


class DeleteRoomView(LoginRequiredMixin, DeleteView):
    model = Room
    success_url = reverse_lazy('list_room')
    template_name = 'planer/room_confirm_delete.html'
    form = DeleteRoomForm
    slug_url_kwarg = 'room_slug'


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'planer/list_room.html'
    context_object_name = 'rooms'
    paginate_by = 9

    search_room_name = ''
    date_room = ''

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):

        self.extra_context = {
            'dates': sorted(list(set(map(lambda x: str(x['date'].date()), Room.objects.all().order_by('date').values('date'))))),
        }
        if self.search_room_name:
            queryset = Room.objects.filter(name__iregex=self.search_room_name)
            self.paginate_by = None
            return queryset
        if self.date_room:
            queryset = Room.objects.filter(date__date__exact=self.date_room)
            self.paginate_by = None
            return queryset
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        self.search_room_name = request.GET.get('room_name')
        self.date_room = request.GET.get('date_room')

        return super().get(self, request, *args, **kwargs)


class MyGamesView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'planer/list_user_room.html'
    context_object_name = 'rooms'
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Room.objects.filter(players__id=self.request.user.id)
        return queryset


class MyRoomsView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'planer/list_master_room.html'
    context_object_name = 'rooms'
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Room.objects.filter(master__id=self.request.user.id)
        return queryset


class AddMessageView(LoginRequiredMixin, FormView):
    form_class = MessageForm
    template_name = 'planer/room.html'
    prefix = 'message'
    success_url = '/'

    def form_valid(self, form):
        form.cleaned_data['author_id'] = self.request.user.id

        r = json.loads(self.request.session['room'])[0]
        slug = r['fields']['slug']
        form.cleaned_data['room_id'] = r['pk']
        m = Message.objects.create(**form.cleaned_data)
        m.save()
        return redirect(Room.objects.get(slug=slug))

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):

        return super().post(request, *args, **kwargs)
