import os
from bs4 import BeautifulSoup

import pymongo
from pymongo import MongoClient
connection = MongoClient('localhost',27017)
db = connection.saregamapa

songs_collection = db.songs_1000

#Second step: Parse the downloaded pages and extract the lyrics, artist, title, and the url of the song
path = r''+os.getcwd()+'\songs'

content_counter = 0

songs_list = []

for name in os.listdir(path):
    f = open(path+'\\'+name, 'r', encoding="utf8")

    contents = f.read()
    if(len(contents) != 0):
        #htmlpage = BeautifulSoup(contents, "html.parser")
        soup = BeautifulSoup(contents, "lxml")


        song_dict = {
            'name': '',
            'artist': '',
            'lyrics': ''
        }
        
        #print(soup.title.string)

        #content = soup.find(id="content_h")

        content = soup.find('div', {"id":"content_h"})

        song_object = soup.title.text.split(' - ')

        song_dict['name'] = song_object[0]
        song_dict['artist'] = song_object[1]

         
        
        if content is not None:
            song_dict['lyrics']  = content.text 

        #songs_list.append(song_dict)        
        songs_collection.insert_one(song_dict)

    f.close()
    
#print(songs_list)
