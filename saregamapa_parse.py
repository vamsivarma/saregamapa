import os
import saregamapa_common as sc
import saregamapa_indexdata as si
import saregamapa_visualize as sv
import saregamapa_search as ss
import saregamapa_mongo as sm
from bs4 import BeautifulSoup

scommon = sc.Saregamapa_Common("Common Utilities")
smongo = sm.Saregamapa_Mongo("saregamapa") 



parse_dict = {
            "songs_collection": "songs_1000",
            "artist_collection": "artists_map_1000",
            "iindex_collection": "iindex_1000",
            "folder_name": "\songs_1000"
        }

smeta = {
            "songs_list": [],
            "artist_dict_list": [],
            "documents_meta": [],
            "sindexes": [],
            "sQuery": "love",
            "clusters_count": 2
            } 

collection_list = smongo.get_db_collections()

class Saregamapa_Parse:

    #@TODO: Need to initialize this with no of records already existing
    songs_list = []
    artist_map = {}
    artist_list = []
    artist_dict_list = []
    songs_collection = ""
    artist_collection = ""
    folder_name = ""   
    
    def get_song_url(self, htmlpage):
        url = ''
    
        for link in htmlpage.find_all('a'):
            if link.get_text() == 'English':
                url = 'https://www.azlyrics.com' + link.get('href') 
                break
    
        return url

    def save_songs_data(self):
        
        self.songs_list = []
        path = r'' + os.getcwd()  + self.folder_name
        doc_index = 1
        
        for name in os.listdir( path ):
            f = open(path+'\\'+name, 'r', encoding="utf8")
        
            contents = f.read()
            if(len(contents) != 0):
        
                song_page = BeautifulSoup(contents, "lxml")
        
                song_dict = {
                    'index': 1,    
                    'title': '',
                    'artist': '',
                    'lyrics': '',
                    'word_count': '',
                    'url': ''
                }
        
                content = song_page.find('div', {"id":"content_h"})
                song_object = song_page.title.text.split(' - ')
                
                artistName = ''
                if(len(song_object) > 1):
                    artistName = song_object[1]    
                
                if artistName in self.artist_map:
                    self.artist_map[artistName] += 1
                else:
                    self.artist_map[artistName] = 1
                
                
                song_dict['index'] = doc_index
                song_dict['title'] = scommon.format_text(song_object[0].replace(' Lyrics', ''))
                song_dict['artist'] = scommon.format_text(artistName)
                song_dict['url'] = self.get_song_url(song_page)
        
                if content is not None:
                    song_dict['lyrics']  = scommon.format_text(content.get_text(separator=' '))
                    song_dict['word_count'] = len(song_dict['lyrics'].split()) 
                    
                    if song_dict['title'] != '' and song_dict['artist'] != '': 
                        self.songs_list.append(song_dict)
                        doc_index += 1
        
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
        
        self.save_songs_data() 
        self.save_artists()
        

if(parse_dict["songs_collection"] not in collection_list):
    sp = Saregamapa_Parse(parse_dict)    
    
smeta["songs_list"] = smongo.get(parse_dict["songs_collection"])
smeta["artist_dict_list"] = smongo.get(parse_dict["artist_collection"])
     
#sv.Saregamapa_Visualize(smeta["songs_list"], smeta["artist_dict_list"])

smeta["documents_meta"] = scommon.get_documents_meta(smeta["songs_list"])

#print(smeta["documents_meta"])


if(parse_dict["iindex_collection"] not in collection_list):
    si.Saregamapa_Indexdata(smeta, smongo, parse_dict["iindex_collection"])

smeta["sindexes"] =  smongo.get(parse_dict["iindex_collection"])

#print(len((smeta["sindexes"][0]).keys()))
#print(smeta["sQuery"])

#Do search
ss.Saregamapa_Search(smeta)






