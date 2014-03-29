from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Artist, Album, Song, VideoType, SongOfTheDay, Discography

artist_extra_fields = ((None, {"fields": ("name",)}),)


class ArtistInline(admin.TabularInline):
    model = Discography

class ArtistAdmin(PageAdmin):
    inlines = (ArtistInline,)
    fieldsets = deepcopy(PageAdmin.fieldsets)

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(SongOfTheDay, ArtistAdmin)
admin.site.register(VideoType)