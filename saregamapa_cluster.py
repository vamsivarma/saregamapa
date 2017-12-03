"""
Created on Tue Nov 21 17:38:54 2017

@author: Vamsi Varma
"""

import math
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Saregamapa_Cluster:
    
    isServer = True
    smeta = {}
    songs_dict = {}
    
    cluster_results = []
        
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
        
        if(self.isServer):        
            print("Documents Intersection: ", intersect)
        
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

        if(self.isServer):
            for i in range(len(intersect)):
                print("song "+str(list(intersect)[i])+" is in cluster "+str(c[i]))
            #we could try it more times to see the best solution, since it isn't optimal
        
        return c
    
    def insert_doc(self, doc_id):
        curDoc = self.songs_dict[str(doc_id)]
        return [curDoc[0], curDoc[0], curDoc[1], curDoc[3]]
    
    def create_wordcloud(self, intersect, c):
        
        #word CLoud
        cluster_diz = {}
        for i in range(len(c)):
            cur_doc_id = list(intersect)[i]
            if c[i] in cluster_diz:
                cluster_diz[c[i]].append(cur_doc_id)
            else:              
                cluster_diz[c[i]] = [cur_doc_id]
        
        for i in range(len(cluster_diz.keys())):
            self.cluster_results.append([])    
        
        for cluster in cluster_diz.keys():
            strg_cloud = " "
            
            for doc in cluster_diz[cluster]:
                strg_cloud += self.songs_dict[str(doc)][4] + " "
                self.cluster_results[int(cluster)].append(self.insert_doc(doc))
            
            #strg_cloud = ' '.join(strg_cloud.split())
            
            wordcloud = WordCloud(width = 300, height = 300, margin = 0, collocations=False).generate(strg_cloud)
            #plt.title("Cluster number: "+str(cluster))
            plt.imshow(wordcloud, interpolation = "bilinear")
            plt.axis("off")
            plt.margins(x=0,y=0)
            plt.savefig("static/wordcloud/cluster_" + str(cluster))

            if(self.isServer):
                plt.show()     
   
    def cluster(self):
        self.cluster_results = []
        
        diz_tf_idf = self.smeta["sindexes"]
        
        intersect = self.search_complete(diz_tf_idf)
        n_doc = self.normalize_results(intersect, diz_tf_idf)
        cluster = self.cluster_documents(n_doc, intersect)
        self.create_wordcloud(intersect, cluster)
        
        return self.cluster_results
          
    def __init__(self, smeta, isServer):
        
        self.isServer = isServer
        self.smeta = smeta
        self.songs_dict = smeta["songs_dict"]
        
        

