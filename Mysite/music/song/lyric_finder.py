import json
import urllib
import xml
from urllib.parse import urljoin
from urllib.request import urlopen
import bs4
from textblob import TextBlob
from fuzzywuzzy import fuzz

def parse_lyric(song_title, artist_name=""):
    title_blob = TextBlob(song_title)
    lyric = "No lyric found"
    en_site = "http://lyrics.wikia.com/api.php?action=lyrics&"
    bn_site = "https://banglasonglyrics.com/?s="

    if str(title_blob.detect_language())!='bn':
        artist_name = artist_name.replace(" ", "%20")
        lyric_url = en_site+"artist="+artist_name+"&song=&fmt=json"
        webpage = urlopen(lyric_url)
        json_obj = json.loads(webpage.read().decode())
        albums = json_obj["albums"]
        prev_match_weight = 0
        current_match_weight = 0
        predicted_song=""
        if albums:
            for album in albums:
                songs = album["songs"]
                #print(album["album"])
                for song in songs:
                    #print("\t"+str(song)+"\t")
                    current_match_weight = int(fuzz.partial_token_sort_ratio(song_title, str(song)))
                    if(current_match_weight>prev_match_weight):
                        predicted_song = song
                        prev_match_weight = current_match_weight

           # print("Predicted song is " + str(predicted_song)+" \tweight"+str(prev_match_weight))
            if prev_match_weight<75:
               # print("Predicted song is Nothing")
                return lyric

            #song_title = predicted_song.replace(" ", "_")
            lyric_url = "https://lyrics.wikia.com/wiki/"+artist_name.replace("%20","_")+":"+predicted_song.replace(" ","_")
            print(lyric_url)
            webpage = urlopen(lyric_url)
            bs_obj = bs4.BeautifulSoup(webpage, 'lxml')
            lyric = bs_obj.find('div', class_="lyricbox").get_text(separator="\n")
            return lyric

    elif str(title_blob.detect_language())=='bn':
        if song_title.__len__() == 0:
            return lyric
        try:
           # req = urllib.request.Request(en_site+urllib.parse.quote(song_title+" lyric"), headers={'User-Agent': "Magic Browser"})
            webpage = urlopen(bn_site+urllib.parse.quote(song_title))
            bs_obj = bs4.BeautifulSoup(webpage, 'lxml')
            cards = bs_obj.find('div', class_="card")
            a= cards.find('a')
            print(a)
            webpage = urlopen(a.get("href"))
            bs_obj = bs4.BeautifulSoup(webpage, 'lxml')
            if bs_obj:
                lyric = bs_obj.find('div', class_="lyrics-content").text
            #print(lyric)
        except:
            song_title = song_title.split(" ")
            song_title.pop()
            song_title = " ".join(word for word in song_title)
            lyric = parse_lyric(song_title)
        return lyric