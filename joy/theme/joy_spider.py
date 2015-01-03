import urllib2

from bs4 import BeautifulSoup


base_url = "http://www.invubu.com"


def scrape(url):
    req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html)
        return soup
    except urllib2.HTTPError, e:
        print ("!!!!!!!!!! 404 : : : " + url)
        return None


def get_listing():
    #get songs from list
    soup = scrape(base_url + "/radio/joyfmfl/playlist/2015-01-02.html")
    if soup is not None:
        urls_group = soup.find_all("div", "result_row")

        for click in urls_group:
            #print click['onclick'].split("'")[1]
            get_artist_details(click['onclick'].split("'")[1])


def get_artist_details(url):
    #print(base_url + url)
    soup = scrape(base_url + url)

    if soup is not None:

        urls_group = soup.find_all("p", "lyrics")

        artist_url = urls_group[0].find_all("a")

        for artist in artist_url:
            if 'artist' in artist['href']:
                get_albums(artist['href'])


def get_albums(url):
    soup = scrape(base_url + url)

    if soup is not None:
        urls_group = soup.find_all("div", "result_row")

        info = soup.find_all("div", id="info_txt")
        for string in info:
            print string.text, string.next_sibling

        for click in urls_group:
            get_album_details(click['onclick'].split("'")[1])


def get_album_details(url):
    soup = scrape(base_url + url)

    if soup is not None:
        #album inserts at this point:
        get_title = soup.find_all("p", "song")

        for title_markup in get_title:
            for album_title in title_markup.find_all("b")[:1]:
                print (album_title.text)


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
                print(cleaned_song)
                #active song - get details
                for link in song_title.find_all("a"):
                    get_song_details(link.get('href'))


def get_song_details(url):
    soup = scrape(base_url + url)

    if soup is not None:
        #audio
        audio = soup.find_all('audio')

        for audio_src in audio:
            print(audio_src.get("src"))

        #video
        iframe = soup.find_all('iframe')

        try:
            for video in iframe:
                if 'youtube' in video['src']:
                    print(video['src'])
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

    print("***** end song ****")


get_listing()


