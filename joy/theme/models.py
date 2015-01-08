from django.db import models
from mezzanine.core.fields import RichTextField

class Artist(models.Model):
    name = models.CharField(max_length=200)
    album = models.ManyToManyField("Album", related_name="Album", blank=True, null=True)
    web_site = models.CharField(max_length=200, blank=True, null=True)
    twitter_handle = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    pinterest = models.CharField(max_length=200, blank=True, null=True)
    google = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    vimeo = models.CharField(max_length=200, blank=True, null=True)
    content = RichTextField(("Content"), blank=True, null=True)
    slug = models.SlugField(max_length=400)

    def __unicode__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=300)
    artist = models.ManyToManyField("Artist", related_name="Artist", blank=True, null=True)
    #album = models.ManyToManyField("Album", related_name="AlbumSong", blank=True, null=True)
    #lyrics = models.FileField(upload_to="lyrics", blank=True, null=True)
    lyrics = models.TextField()
    captions = models.FileField(upload_to="captions", blank=True, null=True)
    content = RichTextField(("Content"), blank=True, null=True)
    video_content = models.CharField(max_length=200, blank=True, null=True)
    video_type = models.ForeignKey("VideoType", blank=True, null=True)
    slug = models.SlugField(max_length=400)
    audio = models.CharField(max_length=600)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=200)
    song = models.ManyToManyField("Song", related_name="Song", blank=True, null=True)
    #cover = models.ImageField(upload_to="artists")
    content = RichTextField(("Content"), blank=True)
    amazon_buy_url = models.CharField(max_length=400, blank=True, null=True)
    itunes_buy_url = models.CharField(max_length=400, blank=True, null=True)
    slug = models.SlugField(max_length=400)

    def __unicode__(self):
        return self.name

class VideoType(models.Model):
    video_type_id = models.SmallIntegerField()
    tech = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % (self.tech)

class SongOfTheDay(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(("Content"), blank=True, null=True)
    song = models.ManyToManyField("Song", related_name="SongOfTheDaySong")
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.title