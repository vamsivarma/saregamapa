"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

import math
import heapq

class Saregamapa_Indexdata:
    
    songs_list = []
    all_lyrics = []
        
    def default_invertedindex(self):
        diz={}
        Id = 1
        
        for s in self.all_lyrics:
            #print(s)    
            for char in set(s.split()):
                if char not in diz:
                    diz[char] = [[Id,s.split().count(char)]]
                else:
                    diz[char].append([Id,s.split().count(char)])
            Id += 1
            
        return diz
    
    def advanced_invertedindex(self, diz):
        
        diz_tf_idf = diz
        for word in diz_tf_idf.values():
            idf= math.log10(len(self.all_lyrics)/len(word))
            for elem in word:
                elem[1]=idf*elem[1]
                
        return diz_tf_idf
    
    def apply_search(self, diz_tf_idf):
        
        q = "love"
        #q = input()
        q = q.split()
        diz_qcos = {}
        diz_norm = {}
        
        for doc in range(1,len(self.all_lyrics)+1):
            #numerator
            num = 0
            for word in q:
                for i in range(len(diz_tf_idf[word])):
                    if diz_tf_idf[word][i][0]==doc:
                        num +=  diz_tf_idf[word][i][1]
            diz_qcos[doc]=num
            #denominator
            norm = 0
            for word in diz_tf_idf.values():
                for i in range(len(word)):
                    if word[i][0]==doc:
                        norm +=  word[i][1]**2
            diz_norm[doc]=math.sqrt(norm)
        #print(diz_qcos)
        #print(diz_norm)
        for doc,num in diz_qcos.items():
            if diz_norm[doc]!=0:
                diz_qcos[doc] = num/(math.sqrt(len(q))*diz_norm[doc])
        return diz_qcos
        
        
    
    def apply_heap_toresults(self, diz_qcos):
        
        h = []
        for elem in diz_qcos.keys():
            heapq.heappush(h,(diz_qcos[elem], elem))
        heapq._heapify_max(h)
        for i in range(10):
            print(heapq.heappop(h))
            heapq._heapify_max(h)
    
    def get_all_lyrics(self):
        for song in self.songs_list:
            self.all_lyrics.append(song['lyrics'])
              
    def __init__(self, songs_list):
        
        self.all_lyrics = []
        self.songs_list = songs_list
        self.get_all_lyrics()
        
        ii = self.default_invertedindex()
        diz_tf_idf = self.advanced_invertedindex(ii)
        diz_qcos = self.apply_search(diz_tf_idf)
        self.apply_heap_toresults(diz_qcos)     
        
      
        
'''
f = 'ciao come stai ? Domani non vengo a scuola.'
d = 'Non pensare agli altri ma a te stesso'
e = 'Domani comportati bene'
lista = []

        


get_all_lyrics()

invoke_utilities()
'''
        

