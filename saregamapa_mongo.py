from pymongo import MongoClient


class Saregamapa_Mongo:

    db = ""
        
    def save(self, cName, data): 
        cObj = self.db[cName]
        
        #@TODO: If there are more records then insert 1000 records at a time
        cObj.insert_many(data)  
    
    
    def get(self, cName):
        return self.db[cName].find()
    
              
    def __init__(self, dbName):
        connection = MongoClient('localhost',27017)
        self.db = connection[dbName]
        
        