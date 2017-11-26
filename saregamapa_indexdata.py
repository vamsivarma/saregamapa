"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

import math
from nltk.tokenize import RegexpTokenizer

class Saregamapa_Indexdata:
    
    documents_meta = []
    
    def insert_doc_index(self, doc, char):
        return [doc[0], doc[1].split().count(char), doc[2], doc[3], doc[4]]
    
    def returnCleanKey(self, word):
        #tokenizer = RegexpTokenizer('[^A-Za-z0-9]+')
        #word = ''.join(tokenizer.tokenize(word)) 
        
        #tokenizer = RegexpTokenizer(r'\w+')
        #word = ''.join(tokenizer.tokenize(word))
        
        word = word.replace(".", "")
        word = word.replace("$", "")
        word = word.replace(" ", "")
        
        return word
        
    def default_invertedindex(self):
        diz={}
        
        for doc in self.documents_meta:
            print(doc)    
            for char in set(doc[1].split()):
                
                char = self.returnCleanKey(char)
                
                if char:
                    if char not in diz:
                        diz[char] = [self.insert_doc_index(doc, char)]
                    else:
                        diz[char].append(self.insert_doc_index(doc, char))
        
        #print(len(diz.keys()))            
        return diz
    
    def advanced_invertedindex(self, diz):
        
        diz_tf_idf = diz
        for key, word in diz_tf_idf.items():
            idf= math.log10(len(self.documents_meta)/len(word))
            for elem in word:
                elem[1]=idf*elem[1]
        return diz_tf_idf
        
    def save_indexes(self, indexesDict, smongo, index_collection):
        smongo.save_one(index_collection, indexesDict)
        
    
    def __init__(self, smeta, smongo, index_collection):
                
        self.documents_meta = smeta["documents_meta"]

        diz = self.default_invertedindex() 
        diz_tf_idf = self.advanced_invertedindex(diz)
        
        #print(diz_tf_idf)
        self.save_indexes(diz_tf_idf, smongo, index_collection)

