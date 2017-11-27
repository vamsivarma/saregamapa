# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:47:39 2017

@author: Vamsi Varma

"""

import matplotlib.pyplot as plt
import operator
from pylab import figure
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

class Saregamapa_Visualize():
    
    artist_map = {}
    songs_dict = {}
    
    def draw_artists_histogram(self):
        authors = sorted(self.artist_map.items(), key = operator.itemgetter(1), reverse = True)   
        values = [x[1] for x in authors]
        fig = figure(figsize=(20,10))
        
        barlist = plt.bar(range(len(authors)), values, color = 'c', width = 1)    
        categories = [y[0] for y in authors]
        plt.xticks(range(len(authors)), categories)
        barlist[0].set_color('g')

    def search_for_popular_words(self):
    
        stop = set(stopwords.words('english'))
        wordsDict = {}
    
        
        #put all the lyrics in a list
        lyricsList = []
        for songId in self.songs_dict:
            lyricsList.append(self.songs_dict[songId][4])
            
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
    
    def search_for_popular_artist_names(self):
        authorDict = {}
    
        for author in self.artist_map:
            
            first_name = author.split(' ', 1)[0]
            
            if first_name in authorDict:
                authorDict[first_name] += 1
            else:
                authorDict[first_name] = 1
        
        first10 = sorted(authorDict.items(), key = operator.itemgetter(1), reverse = True)[:10]
    
        print(first10)
    
    def plot_songs_lengths_histogram(self, wordCountDict):
    
        #histogramof the song lengths
        countList = sorted(wordCountDict.items(), key = operator.itemgetter(1), reverse = True)
        values = [x[1] for x in countList]
        fig = figure(figsize=(20,10))
        barlist = plt.bar(range(len(countList)), values, color = 'c', width = 1)
        category = [y[0] for y in countList]
        plt.xticks(range(len(countList)), category)
        barlist[0].set_color('g')
    
    def song_word_count_with_out_repitition(self):
        
        wordCountDict = {} #length of the song without counting repetitions
        for songId in self.songs_dict:
            curSong = self.songs_dict[songId]
            wordCountDict[curSong[1]]=len(set(curSong[4]))
    
        self.plot_songs_lengths_histogram(wordCountDict)
    
    
    def song_word_count_with_repitition(self):
    
        wordCountDict = {} #length of the song without counting repetitions
        for songId in self.songs_dict:
            curSong = self.songs_dict[songId]
            wordCountDict[curSong[1]] = len(curSong[4])
        
        self.plot_songs_lengths_histogram(wordCountDict)
    
    def get_artist_map(self, artist_list):
        
        a_map = {}
        
        
        for artist in artist_list:
            a_map[artist["artist_name"]] =  artist["songs_count"]   
        
        return a_map
        

    def __init__(self, smeta):
        
        self.songs_dict = smeta["songs_dict"]
        self.artist_map = self.get_artist_map(smeta["artist_dict_list"])

        self.draw_artists_histogram()
        
        self.search_for_popular_words()
        
        self.search_for_popular_artist_names()
        
        self.song_word_count_with_repitition()
        
        self.song_word_count_with_out_repitition()
        
        