"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

import operator
import math
from nltk.tokenize import RegexpTokenizer


class Saregamapa_Indexdata:
    
    songs_dict = {}
    
    chunk_size = 200
    
    def insert_doc_index(self, doc, char):
        return [doc[0], doc[4].split().count(char)]
    
    def returnCleanKey(self, word):        
        word = word.replace(".", "")
        word = word.replace("$", "")
        word = word.replace(" ", "")
        
        return word
    
    def invertLight(self, diz):
        
        for key in diz.keys():
            diz[key] = sorted(diz[key], key=operator.itemgetter(1), reverse=True)
            
            if(len(diz[key]) > self.index_limit):
                diz[key] = diz[key][:self.index_limit]    
                
        return diz
        
    def default_invertedindex(self):
        diz={}
        
        for songId in self.songs_dict:
            #print(doc)
            curSong = self.songs_dict[songId]
            
            for char in set(curSong[4].split()):
                
                char = self.returnCleanKey(char)
                
                if char:
                    if char not in diz:
                        diz[char] = [self.insert_doc_index(curSong, char)]
                    else:
                        diz[char].append(self.insert_doc_index(curSong, char))
                        
        #print(len(diz.keys()))
        
        return self.invertLight(diz)
    
    def advanced_invertedindex(self, diz):
        
        diz_tf_idf = diz
        for key, word in diz_tf_idf.items():
            idf= math.log10(len(self.songs_dict.keys())/len(word))
            for elem in word:
                elem[1]=idf*elem[1]
        return diz_tf_idf
        
    def save_indexes(self, indexesDict, smongo, scommon, index_collection):
        
        chunk_size = self.chunk_size
        
        dict_keys_count = len(indexesDict.keys())
        
        if(dict_keys_count < chunk_size):
            chunk_size = dict_keys_count
            
        
        #Saving chunks of dictionaries with 1000 keys
        for dictChunk in scommon.chunks(indexesDict, chunk_size):
            smongo.save_one(index_collection, dictChunk)
            
    
    def __init__(self, smeta, smongo, scommon, index_collection):
                
        self.songs_dict = smeta["songs_dict"]
        self.index_limit = smeta["index_limit"] 
        self.chunk_size = smeta["chunk_size"] 

        diz = self.default_invertedindex() 
        diz_tf_idf = self.advanced_invertedindex(diz)
        
        #print(diz_tf_idf)
        self.save_indexes(diz_tf_idf, smongo, scommon, index_collection)

