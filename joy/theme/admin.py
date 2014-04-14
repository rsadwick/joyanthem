from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Artist, Album, Song, VideoType, SongOfTheDay

artist_extra_fields = ((None, {"fields": ("name",)}),)


admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(SongOfTheDay)
admin.site.register(VideoType)