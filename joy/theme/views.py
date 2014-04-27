from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.utils.datetime_safe import date
from django.views.generic import ListView, CreateView, DetailView
from requests import request
from joy.theme.models import SongOfTheDay, Artist, Song


class SongList(ListView):

    model = SongOfTheDay
    today = date.today()
    queryset = SongOfTheDay.objects.filter(pub_date__year=today.year, pub_date__month=today.month, pub_date__day=today.day)


class ArtistDetail(DetailView):
    model = Artist

    def get_context_data(self, **kwargs):
        context = super(ArtistDetail, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context

class LinkDetail(DetailView):
    model = SongOfTheDay


def get_captions(request, song_id):
    current_song = get_object_or_404(Song, pk=song_id)
    return HttpResponse(current_song.captions)

