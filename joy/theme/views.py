from django.utils.datetime_safe import date
from django.views.generic import ListView, CreateView, DetailView
from joy.theme.models import SongOfTheDay, Artist

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
