"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

from nltk.tokenize import RegexpTokenizer
from itertools import islice

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

class Saregamapa_Common:
    
    common_message = ''
     
    def format_text(self, lyric): 
        
        # let's clean the lyric using RegexpTokenizer from nltk.tokenize
        tokenizer = RegexpTokenizer(r'\w+')
        
        #Remove punctuation
        lyric = ' '.join(tokenizer.tokenize(lyric))
        
        #Remove stopwords
        lyric = self.remove_stopwords(lyric)
    
        return lyric
    
    def remove_stopwords(self, s):
        
        return  " ".join([word for word in s.split() if word not in stopwords.words('english')])
    
    
    #@TODO: Need to remove this function if not used
    def get_documents_meta(self, songs_list):
        documents_meta = []
        for song in songs_list:
            #Combine all the available strings for a song as one
            #doc_string = song['title'] + ' ' +  song['artist'] + ' ' + song['lyrics']
            doc_string = song['lyrics']
            documents_meta.append([song['index'], doc_string, song['_id'], song['title'], song['url']])
        
        return documents_meta
    
    def generate_dict_fromlist(self, dict_list):
        
        dict_consolidated = {}
        
        for curDict in dict_list:
            
            curDict.pop('_id', None) 
            dict_consolidated.update(curDict)
        
        return dict_consolidated
    
    
    #Create cheunks of the big dictionary based on the size passed
    def chunks(self, data, SIZE=10000):
        it = iter(data)
        
        for i in range(0, len(data), SIZE):
            yield {k:data[k] for k in islice(it, SIZE)}
    
    def __init__(self, s):
        
        self.common_message = s

        
        

