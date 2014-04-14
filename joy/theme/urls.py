from __future__ import unicode_literals

from django.conf.urls import patterns, url


from joy.theme.views import ListView, SongList, ArtistDetail


urlpatterns = patterns("",
   url(r'^newest/$', SongList.as_view()),
   url(r'^artist/(?P<slug>[-_\w]+)/$', ArtistDetail.as_view(), name='artist_detail'),
)