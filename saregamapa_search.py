"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

import math
import heapq

class Saregamapa_Search:
    
    smeta = {}
    songs_dict = {}
        
    def apply_search(self, diz_tf_idf):
        
        q = self.smeta["sQuery"]
       
        q = q.split()
        diz_qcos = {}
        diz_norm = {}
        
        #print(q)
        
        for doc in range(1,len(self.songs_dict.keys())+1):
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
            curDoc = self.songs_dict[str(elem)]
            heapq.heappush(h,(diz_qcos[elem], curDoc[0], curDoc[1], 'https://www.azlyrics.com' + curDoc[3]))
        
        heapq._heapify_max(h)
        for i in range(10):
            print(heapq.heappop(h))
            heapq._heapify_max(h)     
              
    def __init__(self, smeta):
        
        self.smeta = smeta
        self.songs_dict = smeta["songs_dict"]
        diz_tf_idf = smeta["sindexes"]
                
        diz_qcos = self.apply_search(diz_tf_idf)
        self.apply_heap_toresults(diz_qcos)           
        

