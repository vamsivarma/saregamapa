import pymongo

from pymongo import MongoClient

connection = MongoClient('localhost',27017)

db = connection.saregamapa
pagesList = db.pages
for page in pagesList.find():
        print(page)

