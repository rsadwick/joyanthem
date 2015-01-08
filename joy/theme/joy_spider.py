import urllib2

from bs4 import BeautifulSoup
#from joy.theme.models import Artist, Album, Song
from .models import Artist, Album, Song
from django.template.defaultfilters import slugify

class JoySpider(object):

    def __init__(self):
        #start up
        self.base_url = "http://www.invubu.com"
        self.get_listing()


    def scrape(self, url):
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html)
            return soup
        except urllib2.HTTPError, e:
            print ("!!!!!!!!!! 404 : : : " + url)
            return None


    def get_listing(self):
        #get songs from list
        soup = self.scrape(self.base_url + "/radio/joyfmfl/playlist/2015-01-02.html")
        if soup is not None:
            urls_group = soup.find_all("div", "result_row")

            for click in urls_group:
                self.get_artist_details(click['onclick'].split("'")[1])


    def get_artist_details(self, url):
        soup = self.scrape(self.base_url + url)

        if soup is not None:
            urls_group = soup.find_all("p", "lyrics")
            artist_url = urls_group[0].find_all("a")

            for artist in artist_url:
                if 'artist' in artist['href']:
                    self.get_albums(artist['href'])


    def get_albums(self, url):
        soup = self.scrape(self.base_url + url)

        if soup is not None:
            urls_group = soup.find_all("div", "result_row")

             #artist_name
            get_artist_name = soup.find_all("p", "song")

            for name_markup in get_artist_name:
                for artist_name in name_markup.find_all("b")[:1]:
                    artist_slug = slugify(artist_name.text)

                    #insert artist by slug
                    current_artist, created = Artist.objects.get_or_create(slug=artist_slug)
                    current_artist.name = artist_name.text
                    print(artist_name.text)

            info = soup.find_all("div", id="info_txt")

            #artist about
            for string in info:
                current_artist.content = string.text, string.next_sibling
                current_artist.save()


            for click in urls_group:
                self.get_album_details(click['onclick'].split("'")[1], artist_slug)
                print('done')


    def get_album_details(self, url, artist_slug):
        soup = self.scrape(self.base_url + url)

        if soup is not None:
            #album inserts at this point:
            get_title = soup.find_all("p", "song")

            for title_markup in get_title:
                for album_title in title_markup.find_all("b")[:1]:
                    print (album_title.text)
                    album_slug = slugify(album_title.text)
                    current_album, created = Album.objects.get_or_create(slug=album_slug)
                    current_album.name = album_title.text

                    #artist_id = Artist.objects.get(slug=artist_slug).id

                    current_album.save()

                    album_id = Album.objects.get(slug=album_slug).id
                    current_artist2 = Artist.objects.get(slug=artist_slug)

                    current_artist2.album.add(Album.objects.get(pk=album_id))
                    current_artist2.save()

            #urls for buying the music
            get_urls = soup.find_all("a")
            for album_url in get_urls:
                try:
                    if 'itunes' in album_url['href']:
                        print(album_url['href'].split('?')[0])

                    if 'amazon' in album_url['href']:
                        print(album_url['href'].split('&tag')[0])

                    if 'play.google' in album_url['href']:
                        print(album_url['href'])

                except KeyError, e:
                    d = e

            #snag songs
            get_songs = soup.find_all(id="album_songs_txt")
            print("***** song ****")
            for song_title in get_songs:
                for cleaned_song in song_title.find_all("td")[1]:
                    print("***** !!!! songy ***** ")
                    #other songs - insert title
                    #song_text = cleaned_song.text
                    #active song - get details
                    for link in song_title.find_all("a"):
                        self.get_song_details(link.get('href'), artist_slug, album_slug, link.text)



    def get_song_details(self, url, artist_slug, album_slug, song_name):
        soup = self.scrape(self.base_url + url)


        if soup is not None:

            #start building song:
            song_slug = slugify(song_name)
            current_song, created = Song.objects.get_or_create(slug=song_slug)
            current_song.name = song_name

            #audio
            audio = soup.find_all('audio')

            for audio_src in audio:
                print(audio_src.get("src"))
                current_song.audio = audio_src.get("src")

            #video
            iframe = soup.find_all('iframe')

            try:
                for video in iframe:
                    if 'youtube' in video['src']:
                        print(video['src'])
                        current_song.video_content = video['src']
            except KeyError, e:
                d = e

            get_urls = soup.find_all("a")
            for song_url in get_urls:
                try:
                    if 'itunes' in song_url['href']:
                        print(song_url['href'].split('?')[0])

                    if 'amazon' in song_url['href']:
                        print(song_url['href'].split('&tag')[0])

                    if 'play.google' in song_url['href']:
                        print(song_url['href'])

                except KeyError, e:
                    d = e

            #lyrics
            get_lyrics = soup.find_all(id="lyrics_txt")
            for lyrics in get_lyrics:
                current_song.lyrics = lyrics.find_all("p", "lyrics")


            album_id = Album.objects.get(slug=album_slug).id
            artist_id = Artist.objects.get(slug=artist_slug).id
            current_song.artist.add(Artist.objects.get(pk=artist_id))
            current_song.save()

            #saved_song = Song.objects.get(slug=song_slug)

            #artist_id = Artist.objects.get(slug=artist_slug).id


            #saved_song.save()



            song_id = Song.objects.get(slug=song_slug).id
            #add song to album
            current_album = Album.objects.get(slug=album_slug)
            current_album.song.add(Song.objects.get(pk=song_id))
            current_album.save()





        print("***** end song ****")