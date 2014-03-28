from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Artist, Album, Song, VideoType, SongOfTheDay

artist_extra_fields = ((None, {"fields": ("name",)}),)

class SongOfDayInline(admin.TabularInline):
    model = SongOfTheDay

class AlbumInline(admin.TabularInline):
    model = Album

class SongInline(admin.TabularInline):
    model = Song

class ArtistAdmin(PageAdmin):
    inlines = (SongInline,)
    fieldsets = deepcopy(PageAdmin.fieldsets) + artist_extra_fields

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(SongOfTheDay, ArtistAdmin)
admin.site.register(VideoType)