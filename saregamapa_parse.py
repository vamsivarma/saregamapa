import os, nltk
import saregamapa_indexdata as si
import saregamapa_visualize as sv
import saregamapa_mongo as sm


from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
nltk.download('stopwords')

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

smongo = sm.Saregamapa_Mongo("saregamapa") 

class Saregamapa_Parse:

    #@TODO: Need to initialize this with no of records already existing
    songs_list = []
    artist_map = {}
    artist_list = []
    artist_dict_list = []
    songs_collection = ""
    artist_collection = ""
    folder_name = ""
    
    def get_song_lyrics(self, lyric):
        # let's clean the lyric using RegexpTokenizer from nltk.tokenize
        tokenizer = RegexpTokenizer(r'\w+')
        
        #Remove punctuation
        lyric = ' '.join(tokenizer.tokenize(lyric))
        
        #Remove stopwords
        lyric = self.remove_stopwords(lyric)
    
        return lyric
    
    def remove_stopwords(self, s):
        
        return  "  ".join([word for word in s.split() if word not in stopwords.words('english')])   
    
    def get_song_url(self, htmlpage):
        url = ''
    
        for link in htmlpage.find_all('a'):
            if link.get_text() == 'English':
                url = 'https://www.azlyrics.com' + link.get('href') 
                break
    
        return url

    def get_songs_data(self):
        
        self.songs_list = []
        page_index = 0 # Need to set this to current number of records existing in the collection
        path = r'' + os.getcwd()  + self.folder_name
        
        for name in os.listdir( path ):
            f = open(path+'\\'+name, 'r', encoding="utf8")
        
            contents = f.read()
            if(len(contents) != 0):
        
                #content_counter += 1
                song_page = BeautifulSoup(contents, "lxml")
        
                song_dict = {
                    'index': 0,
                    'title': '',
                    'artist': '',
                    'lyrics': '',
                    'word_count': '',
                    'url': ''
                }
        
                content = song_page.find('div', {"id":"content_h"})
                song_object = song_page.title.text.split(' - ')
                artistName = song_object[1]
                
                if artistName in self.artist_map:
                    self.artist_map[artistName] += 1
                else:
                    self.artist_map[artistName] = 1
        
                song_dict['index'] = page_index    
                song_dict['title'] = song_object[0].replace(' Lyrics', '')
                song_dict['artist'] = artistName
                song_dict['url'] = self.get_song_url(song_page)
        
                if content is not None:
                    song_dict['lyrics']  = self.get_song_lyrics(content.text)
                    song_dict['word_count'] = len(song_dict['lyrics'].split()) 
        
                self.songs_list.append(song_dict)        
                
                page_index += 1
        
            f.close()
        
        smongo.save(self.songs_collection, self.songs_list)
        
            
    def save_artists(self): 
        
        self.artist_dict_list = []
        
        for artist in self.artist_map:
            artist_dict = {
                'artist_name': artist,
                'songs_count': self.artist_map[artist]
            }
            
            self.artist_list.append(artist)
            
            self.artist_dict_list.append(artist_dict)
        

        smongo.save(self.artist_collection, self.artist_dict_list)


    def __init__(self, pObj):
        
        self.songs_collection = pObj["songs_collection"]
        self.artist_collection = pObj["artist_collection"]
        self.folder_name = pObj["folder_name"]
        
        self.get_songs_data() 
        self.save_artists()



parse_dict = {
            "songs_collection": "songs_1000",
            "artist_collection": "artists_map_1000",
            "folder_name": "\songs_1000"
        }

sp = Saregamapa_Parse(parse_dict)

sv.Saregamapa_Visualize(sp.songs_list, sp.artist_map)

si.Saregamapa_Indexdata(sp.songs_list)
