import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from pymongo import MongoClient
import matplotlib.pyplot as plt
from pylab import figure
from nltk.corpus import stopwords
import operator
import nltk
nltk.download('stopwords')

connection = MongoClient('localhost', 27017)
db = connection.saregamapa
songs_collection = db.songs_1000
artist_collection = db.artists_map_1000

path = r'' + os.getcwd() + '\songs_10'

#@TODO: Need to initialize this with no of records already existing
page_index = 0
songs_list = []
artist_map = {}
artist_list = []

def get_song_lyrics(lyric):
    # let's clean the lyric using RegexpTokenizer from nltk.tokenize
    tokenizer = RegexpTokenizer(r'\w+')
    lyric = ' '.join(tokenizer.tokenize(lyric))

    return lyric

def get_song_url(htmlpage):
    url = ''

    for link in htmlpage.find_all('a'):
        if link.get_text() == 'English':
            url = 'https://www.azlyrics.com' + link.get('href') 
            break

    return url 

def draw_artists_histogram():
    authors = sorted(artist_map.items(), key = operator.itemgetter(1), reverse = True)   
    values = [x[1] for x in authors]
    fig = figure(figsize=(20,10))
    
    barlist = plt.bar(range(len(authors)), values, color = 'c', width = 1)    
    categories = [y[0] for y in authors]
    plt.xticks(range(len(authors)), categories)
    barlist[0].set_color('g')

def search_for_popular_words():

    stop = set(stopwords.words('english'))
    wordsDict = {}

    
    #put all the lyrics in a list
    lyricsList = []
    for song in songs_list:
        lyricsList.append(song['lyrics'])
        
    #for every song lyric
    for lyric in lyricsList:
        # removing all the stopwords from the lyric i
        iNoStop = lyric
        for i in stop:
            lyricWords = iNoStop.split()
            for e in range(len(lyricWords)):
                if(i.lower() == lyricWords[e].lower()): 
                    lyricWords[e] = ''
                                
            iNoStop = ' '.join(lyricWords)
        
        #updating the dictionary containing all the words
        for p in iNoStop.split():
            if(p.lower().strip() in wordsDict.keys()):
                wordsDict[p.lower()] += 1
            else:
                wordsDict[p.lower()] = 1
                            

    # this return the 20 most popular words (exclude stopwords)
    first20 = sorted(wordsDict.items(), key = operator.itemgetter(1), reverse = True)[:20]

    # this is the  histogram of the number of occurence per word for the 20 most popular words
    values2 = [x[1] for x in first20]
    fig=figure(figsize=(20,10))
    barlist2 = plt.bar(range(len(first20)),values2, color = 'c')
    category2 = [y[0] for y in first20]
    plt.xticks(range(len(first20)), category2)
    barlist2[0].set_color('g')

def search_for_popular_artist_names():
    authorDict = {}

    for author in artist_map:
        
        first_name = author.split(' ', 1)[0]
        
        if first_name in authorDict:
            authorDict[first_name] += 1
        else:
            authorDict[first_name] = 1
    
    first10 = sorted(authorDict.items(), key = operator.itemgetter(1), reverse = True)[:10]

    print(first10)

def plot_songs_lengths_histogram(wordCountDict):

    #histogramof the song lengths
    countList = sorted(wordCountDict.items(), key = operator.itemgetter(1), reverse = True)
    values = [x[1] for x in countList]
    fig=figure(figsize=(20,10))
    barlist = plt.bar(range(len(countList)), values, color = 'c', width = 1)
    category = [y[0] for y in countList]
    plt.xticks(range(len(countList)), category)
    barlist[0].set_color('g')

def song_word_count_with_out_repitition():
    
    wordCountDict = {} #length of the song without counting repetitions
    for song in songs_list:
        wordCountDict[song['title']]=len(set(song['lyrics']))

    plot_songs_lengths_histogram(wordCountDict)


def song_word_count_with_repitition():

    wordCountDict = {} #length of the song without counting repetitions
    for song in songs_list:
        wordCountDict[song['title']] = len(song['lyrics'])
    
    plot_songs_lengths_histogram(wordCountDict)    


for name in os.listdir(path):
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
        
        if artistName in artist_map:
            artist_map[artistName] += 1
        else:
            artist_map[artistName] = 1

        song_dict['index'] = page_index    
        song_dict['title'] = song_object[0].replace(' Lyrics', '')
        song_dict['artist'] = artistName
        song_dict['url'] = get_song_url(song_page)

        if content is not None:
            song_dict['lyrics']  = get_song_lyrics(content.text)
            song_dict['word_count'] = len(song_dict['lyrics'].split()) 

        songs_list.append(song_dict)        
        #songs_collection.insert_one(song_dict)
        page_index += 1

    f.close()

artist_dict_list = []

for artist in artist_map:
    artist_dict = {
        'artist_name': artist,
        'songs_count': artist_map[artist]
    }
    artist_list.append(artist)
    artist_dict_list.append(artist_dict)

    #artist_collection.insert_one(artist_dict)

draw_artists_histogram()

search_for_popular_words()

search_for_popular_artist_names()

song_word_count_with_repitition()

song_word_count_with_out_repitition()


