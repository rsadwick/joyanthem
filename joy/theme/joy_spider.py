from bs4 import BeautifulSoup
import urllib2

#BASE_URL = "http://www.invubu.com/radio/joyfmfl/playlist.html?refresh=no"
#html = urlopen(BASE_URL).read()
#soup = BeautifulSoup(html)
#urls_group = soup.find_all("div", "result_row")

#print(urls_group)
base_url = "http://www.invubu.com"
def scrape(url):
    req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib2.urlopen(req).read()
    #html = urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

def get_listing():
    #get songs from list
    soup = scrape(base_url + "/radio/joyfmfl/playlist.html?refresh=no")
    urls_group = soup.find_all("div", "result_row")

    for click in urls_group:
        #print click['onclick'].split("'")[1]
        get_artist_details(click['onclick'].split("'")[1])


def get_artist_details(url):
    #print(base_url + url)
    soup = scrape(base_url + url)
    urls_group = soup.find_all("p", "lyrics")

    artist_url = urls_group[0].find_all("a")

    for artist in artist_url:
        if 'artist' in artist['href']:
            get_albums(artist['href'])

    #get artist details
    #album image
    #website
    #description
    #albums
    #print('listing')

def get_albums(url):
    soup = scrape(base_url + url)
    urls_group = soup.find_all("div", "result_row")


    for click in urls_group:
        print (click['onclick'].split("'")[1])
    #itunes/amazon/google play?
    #song

def get_album_details():
    #album inserts at this point:
    #name
    #image
    #itunes/amazon/play

    #search for songs - request song page

def get_song_details():
    #title
    #mp4
    #itunes/amazon/google play
    #video
    #lyrics
    print('listing')


get_listing()


