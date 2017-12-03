import saregamapa_common as sc
import saregamapa_mongo as sm
import saregamapa_parse as sp
import saregamapa_indexdata as si
import saregamapa_search as ss
import saregamapa_cluster as scc   
import saregamapa_visualize as sv     

class Saregamapa_Index:
    
    parse_dict = {
            "songs_collection": "songs_1000",
            "artist_collection": "artists_map_1000",
            "iindex_collection": "iindex_1000",
            "folder_name": "\songs_complete\lyrics_collection",
            "max_records": 1000
        }

    smeta = {
                "songs_dict": {},
                "artist_dict_list": [],
                "documents_meta": [],
                "sindexes": {},
                "index_limit": 200,
                "sQuery": "night",
                "clusters_count": 2,
                "chunk_size": 1000
                } 
    
    scommon = {}
    smongo = {}
    collection_list = [] 

    def parse_data(self):
        if(self.parse_dict["songs_collection"] not in self.collection_list):
            sp.Saregamapa_Parse(self.parse_dict, self.smongo, self.scommon, self.smeta)    

        self.smeta["songs_dict"] = self.scommon.generate_dict_fromlist(self.smongo.get(self.parse_dict["songs_collection"])) 
        self.smeta["artist_dict_list"] = self.smongo.get(self.parse_dict["artist_collection"])
    
    def visualize_data(self):
        sv.Saregamapa_Visualize(self.smeta)        
    
    def do_indexing(self):
        if(self.parse_dict["iindex_collection"] not in self.collection_list):
            si.Saregamapa_Indexdata(self.smeta, self.smongo, self.scommon, self.parse_dict["iindex_collection"])

        self.smeta["sindexes"] =  self.scommon.generate_dict_fromlist(self.smongo.get(self.parse_dict["iindex_collection"]))      

    def apply_search(self, query, isServer):
        
        self.smeta["sQuery"] = query
        
        #Do search
        ssearch = ss.Saregamapa_Search(self.smeta)
        
        if(isServer):
            print(ssearch.search())
        else:
            return ssearch.search()
    
    def cluster_data(self, query, clusters_count, isServer):
        self.smeta["sQuery"] = query
        self.smeta["clusters_count"] = clusters_count
               
        #Do Clustering
        scluster = scc.Saregamapa_Cluster(self.smeta, isServer)
        
        return scluster.cluster()
    
    def __init__(self):
        
        self.scommon = sc.Saregamapa_Common("Common Utilities")
        self.smongo = sm.Saregamapa_Mongo("saregamapa")
        self.collection_list = self.smongo.get_db_collections()
        
        self.parse_data()
        #self.visualize_data()
        self.do_indexing()
        
        #self.apply_search("love", True)
        #self.cluster_data("love", 2, True)


#Starting point of the application        
sIndex = Saregamapa_Index()    