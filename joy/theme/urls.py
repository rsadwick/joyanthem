from __future__ import unicode_literals

from django.conf.urls import patterns, url


from joy.theme.views import ListView, SongList, ArtistDetail, get_captions, SongOfTheDayList, AllArtistList, browse


urlpatterns = patterns("",
   url(r'^newest/$', SongList.as_view()),
   url(r'^artist/(?P<slug>[-_\w]+)/$', ArtistDetail.as_view(), name='artist_detail'),
   url(r'^services/(?P<song_id>[0-9]+)/$', get_captions, name='get_captions'),
   url(r'^sotd/$', SongOfTheDayList.as_view(), name='songoftheday_listing'),
   url(r'^artists/$', AllArtistList.as_view(), name='get_artists'),
   url(r'^browse/$', browse, name='browse'),
)