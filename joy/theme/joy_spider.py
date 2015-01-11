import urllib2
import tinys3
from bs4 import BeautifulSoup
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

    def insert_images(self, local_image, image_url):
        #download image from envato
        image_file = open(local_image, 'wb')
        img_url = 'http://' + image_url.split('://')[-1]
        image_file.write(urllib2.urlopen(img_url).read())
        image_file.close()

        #upload to s3
        aws_connection = tinys3.Connection('AKIAJNJVDJ2TL75JXGTA', 'nwB4Oo+HXNbeZRYhxRvy1N+ry9W+EPu/cFFBq2sk', tls=True, endpoint='s3.amazonaws.com')
        file = open(local_image, 'rb')
        aws_connection.upload(local_image, file, 'img.joyanthem.com/album_art')


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
            urls_group = soup.find_all(id="solo_albums_txt")

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

            #all_albums = urls_group.
            for click in urls_group:
                album_rows = click.find_all("div", "result_row")
                for album in album_rows:

                    self.get_album_details(album['onclick'].split("'")[1], artist_slug)
                    print('done')


    def get_album_details(self, url, artist_slug):
        soup = self.scrape(self.base_url + url)

        if soup is not None:
            #album inserts at this point:
            get_title = soup.find_all("p", "song")

            for title_markup in get_title:
                for album_title in title_markup.find_all("b")[:1]:
                    print (album_title.text)
                    #save album info
                    album_slug = slugify(album_title.text)
                    current_album, created = Album.objects.get_or_create(slug=album_slug)
                    current_album.name = album_title.text
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
                        current_album.itunes_buy_url = album_url['href'].split('?')[0]
                        #print(album_url['href'].split('?')[0])

                    if 'amazon' in album_url['href']:
                        current_album.amazon_buy_url = album_url['href'].split('&tag')[0]
                        #print(album_url['href'].split('&tag')[0])

                    if 'play.google' in album_url['href']:
                        current_album.google_buy_url = album_url['href']
                        #print(album_url['href'])

                except KeyError, e:
                    pass


            #save album:
            #current_album.save()


            #snag songs
            get_songs = soup.find_all(id="album_songs_txt")

            for song_title in get_songs:
                for anchor in song_title.find_all("td"):
                    #pull out href to song and song name
                    if anchor.a is not None:
                        self.get_song_details(anchor.a['href'], artist_slug, album_slug, anchor.a.text, True)
                    else:
                        #songs that dont have href get inserted with name/slug and also skips to second TD
                        song_name = anchor.find_next_sibling()
                        if song_name is not None:
                            self.get_song_details(None, artist_slug, album_slug, song_name.get_text(), False)


    def get_song_details(self, url, artist_slug, album_slug, song_name, isPlayed):
        #start building song:
        song_slug = slugify(song_name)
        current_song, created = Song.objects.get_or_create(slug=song_slug)
        current_song.name = song_name

        #query album that the song lives on
        current_album = Album.objects.get(slug=album_slug)

        if isPlayed == True:
            soup = self.scrape(self.base_url + url)

            if soup is not None:

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
                    pass

                get_urls = soup.find_all("a")
                for song_url in get_urls:
                    try:
                        if 'itunes' in song_url['href']:
                            current_song.itunes_url = song_url['href'].split('?')[0]

                        if 'amazon' in song_url['href']:

                            removal_part = 'invubu-20'
                            amazon_url = song_url['href'].split('&tag')[0]
                            if amazon_url.endswith(removal_part):
                                amazon_url = url[:-len(removal_part)]

                            current_song.amazon_url = amazon_url

                        if 'play.google' in song_url['href']:
                            current_song.google_url = song_url['href']

                    except KeyError, e:
                        pass

                #snag artist image
                soup_to_str = str(soup)
                image_url = soup_to_str.split('var image_src500 =', 1)[1]
                image_url = image_url.split(";")[0]
                image_url = image_url.replace("'", "")
                image_url = image_url.replace(" ", "")

                img_domain = 'http://www.invubu.com'
                absolute_img_url =  img_domain + image_url
                print absolute_img_url
                #only image name + ext
                image_src = image_url.rsplit('/', 1)[1]

                current_album.art = 'album_art/' + image_src
                #download image and insert into s3
                self.insert_images(image_src, absolute_img_url)

                #lyrics
                get_lyrics = soup.find_all(id="lyrics_txt")
                for lyrics in get_lyrics:
                    current_song.lyrics = lyrics.find_all("p", "lyrics")

        #artist id
        artist_id = Artist.objects.get(slug=artist_slug).id
        #add artist to song
        current_song.artist.add(Artist.objects.get(pk=artist_id))
        current_song.save()
        #get song id
        song_id = Song.objects.get(slug=song_slug).id
        #add song to album

        current_album.song.add(Song.objects.get(pk=song_id))
        current_album.save()

        print("***** end song ****")