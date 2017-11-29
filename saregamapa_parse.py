import os
from bs4 import BeautifulSoup


class Saregamapa_Parse:

    songs_dict = {}
    artist_map = {}
    artist_list = []
    artist_dict_list = []
    
    songs_collection = ""
    artist_collection = ""
    folder_name = "" 
    
    chunk_size = 200
    
    max_records = 1
    
    def get_song_url(self, htmlpage):
        url = ''
    
        for link in htmlpage.find_all('a'):
            if link.get_text() == 'English':
                url = link.get('href') 
                break
    
        return url

    def save_songs_data(self, smongo, scommon):
        
        self.songs_dict = {}
        path = r'' + os.getcwd()  + self.folder_name
        doc_index = 1
        
        for name in os.listdir( path ):
            f = open(path+'\\'+name, 'r', encoding="utf8")
        
            contents = f.read()
            if(len(contents) != 0):
        
                song_page = BeautifulSoup(contents, "lxml")
                
                self.songs_dict[str(doc_index)] = []
        
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
                        
                        self.songs_dict[str(doc_index)] = [song_dict['index'], song_dict['title'], song_dict['artist'], song_dict['url'], song_dict['lyrics'], song_dict['word_count']]
                        doc_index += 1
        
            f.close()
            
            if doc_index > self.max_records:
                break
        
        self.save_songs(smongo, scommon)
        
    
    def save_songs(self, smongo, scommon):
       
        chunk_size = self.chunk_size
        
        dict_keys_count = len(self.songs_dict.keys())
        
        if(dict_keys_count < chunk_size):
            chunk_size = dict_keys_count
        
        #Saving chunks of dictionaries with 1000 keys
        for songChunk in scommon.chunks(self.songs_dict, chunk_size):
            smongo.save_one(self.songs_collection, songChunk)
            
    def save_artists(self, smongo): 
        
        self.artist_dict_list = []
        
        for artist in self.artist_map:
            artist_dict = {
                'artist_name': artist,
                'songs_count': self.artist_map[artist]
            }
            
            self.artist_list.append(artist)
            
            self.artist_dict_list.append(artist_dict)
        
        smongo.save(self.artist_collection, self.artist_dict_list)


    def __init__(self, pObj, smongo, scommon, smeta):
        
        self.songs_collection = pObj["songs_collection"]
        self.artist_collection = pObj["artist_collection"]
        self.folder_name = pObj["folder_name"]
        
        self.max_records = pObj["max_records"]
        self.chunk_size =  smeta["chunk_size"]
        
        self.save_songs_data(smongo, scommon) 
        self.save_artists(smongo)
        



