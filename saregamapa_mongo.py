from pymongo import MongoClient


class Saregamapa_Mongo:

    db = ""
        
    def save(self, cName, data): 
        cObj = self.db[cName]
        
        #@TODO: If there are more records then insert 1000 records at a time
        cObj.insert_many(data)  
    
    def save_one(self, cName, data): 
        cObj = self.db[cName]
        
        cObj.insert_one(data)
    
    def get(self, cName):
        
        data = list(self.db[cName].find({}))
        result = []
        
        for d in data:
            result.append(d)
        
        return result
    
    def get_db_collections(self):
        return self.db.collection_names(include_system_collections=False)
          
    def __init__(self, dbName):
        connection = MongoClient('localhost',27017)
        self.db = connection[dbName]
        
        