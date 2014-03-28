from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import RichTextField


class SongOfTheDay(Page):
    name = models.CharField(max_length=100)
    song = models.ForeignKey("Song", blank=True, null=True)

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    web_site = models.CharField(max_length=200)
    twitter_handle = models.CharField(max_length=100)
    facebook = models.CharField(max_length=200)
    pinterest = models.CharField(max_length=200)
    google = models.CharField(max_length=200)
    youtube = models.CharField(max_length=200)
    vimeo = models.CharField(max_length=200)
    content = RichTextField(("Content"), blank=True)

    def __unicode__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=300)
    artist = models.ForeignKey("Artist", null=True)
    album = models.ForeignKey("Album", blank=True, null=True)
    lyrics = models.FileField(upload_to="lyrics", blank=True, null=True)
    captions = models.FileField(upload_to="captions", blank=True, null=True)
    content = RichTextField(("Content"), blank=True, null=True)
    video_content = models.CharField(max_length=200)
    video_type = models.ForeignKey("VideoType")
    day = models.ForeignKey(SongOfTheDay, related_name='SongOfTheDay')

    def __unicode__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ForeignKey("Artist", blank=True, null=True)
    #cover = models.ImageField(upload_to="artists")
    content = RichTextField(("Content"), blank=True)

    def __unicode__(self):
        return self.name


class VideoType(models.Model):
    video_type_id = models.SmallIntegerField()
    tech = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % (self.tech)
