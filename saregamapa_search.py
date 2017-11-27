"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

import math
import heapq
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
            heapq.heappush(h,(diz_qcos[elem], curDoc[0], curDoc[1], curDoc[3]))
        
        heapq._heapify_max(h)
        for i in range(10):
            print(heapq.heappop(h))
            heapq._heapify_max(h)
    
    def search_complete(self, diz):
        
        #print("Inside search complete")
        ###return all the songs that contain all the query terms
        q = self.smeta["sQuery"]
        #ask query
        #q = input("Insert query: ")
        q = q.split()
        #create a dictionary word of the query(key): in wich song it is in(value)
        diz_intersect = {}
        for query in q:
            for word in diz.keys():
                if query==word:
                    for i in range(len(diz[word])):
                        if query not in diz_intersect:
                            diz_intersect[query] = [diz[word][i][0]]
                        else:
                            diz_intersect[query].append(diz[word][i][0])
                            
        #create a set of all the songs that contain all the query terms
        intersect = diz_intersect[q[0]]
        for i in range(1,len(q)):
            if i == len(q):
                break
            else:
                intersect = set(intersect).intersection(diz_intersect[q[i]])
        #print(intersect)
        
        return intersect
        
    def normalize_results(self, intersect, diz_tf_idf):
        #Normalize the vector
        data = []
        #for every document in the intersection create a list where every element(associated to a word) is it's tf-idf normalized
        for doc in intersect:
            #diz_normalized is a dictionary word(key): with it's tf-idf normalized(value)
            diz_normalized = {}
            #norm of the document: denominator
            doc_norm = 0
            for word in diz_tf_idf.keys():
                for i in range(len(diz_tf_idf[word])):
                    if doc == diz_tf_idf[word][i][0]:
                        diz_normalized[word] = diz_tf_idf[word][i][1]
                        doc_norm += diz_tf_idf[word][i][1]**2
            #print(diz_normalized)
            #print(doc_norm)
            #create the vector desired and put it in a array
            for w in diz_normalized.keys():
                diz_normalized[w] = diz_normalized[w]/math.sqrt(doc_norm)
            #print(diz_normalized)
            l = []
            for word in diz_tf_idf.keys():
                if word in diz_normalized:
                    l.append(diz_normalized[word])
                else:
                    l.append(0)
            #print(l)
            data.append(l)
        
        #print(data)
        return data
    
    def cluster_documents(self, data, intersect):
         
        #HOW MANY CLUSTERS?
        #k = int(input("How many clusters? "))
        k = self.smeta["clusters_count"]
        
        #use k-means to clusterize the songs
        kmeans = KMeans(n_clusters=k, init='random') # initialization
        kmeans.fit(data) # actual execution
        c = kmeans.predict(data)
        #print(c.shape)
        #print(c)
        #for i in range(len(intersect)):
            #print("song "+str(list(intersect)[i])+" is in cluster "+str(c[i]))
        #we could try it more times to see the best solution, since it isn't optimal
        
        return c
    
    def create_wordcloud(self, intersect, c):
        
        #word CLoud
        cluster_diz = {}
        for i in range(len(c)):
            if c[i] in cluster_diz:
                cluster_diz[c[i]].append(list(intersect)[i])
            else:
                cluster_diz[c[i]] = [list(intersect)[i]]
        #print(cluster_diz)
        for cluster in cluster_diz.keys():
            strg_cloud = " "
            for doc in cluster_diz[cluster]:
                strg_cloud += self.songs_dict[str(doc)][4] + " "
            
            #strg_cloud = ' '.join(strg_cloud.split())
            
            wordcloud = WordCloud(width = 480, height = 480, margin = 0, collocations=False).generate(strg_cloud)
            plt.title("Cluster number: "+str(cluster))
            plt.imshow(wordcloud, interpolation = "bilinear")
            plt.axis("off")
            plt.margins(x=0,y=0)
            plt.show()        
              
    def __init__(self, smeta, scommon):
        
        self.smeta = smeta
        self.songs_dict = smeta["songs_dict"]
        
        diz_tf_idf = scommon.generate_dict_fromlist(smeta["sindexes"])
        
        #print(diz_tf_idf)
                
        diz_qcos = self.apply_search(diz_tf_idf)
        self.apply_heap_toresults(diz_qcos)
        
        intersect = self.search_complete(diz_tf_idf)
        n_doc = self.normalize_results(intersect, diz_tf_idf)
        cluster = self.cluster_documents(n_doc, intersect)
        self.create_wordcloud(intersect, cluster)
        
        

