import matplotlib.pyplot as plt
from pylab import figure
from pymongo import MongoClient
from nltk.corpus import stopwords
import operator


connection = MongoClient('localhost',27017)
db = connection.saregamapa



###First Query
AuthorDict = {}

artists = db.lyrics.find( {},{ '_id':0, 'artist': 1 } )
artistsl = []
for i in artists:
    artistsl.append(i['artist'])
for i in set(artistsl):
    AuthorDict[i] = artistsl.count(i)

# this is the  histogram of the number of songs per Artist
Authors = sorted(AuthorDict.items(), key = operator.itemgetter(1), reverse = True)
values = [x[1] for x in Authors]
fig=figure(figsize=(20,10))
barlist = plt.bar(range(len(Authors)),values, color = 'c', width = 1)
cathegorie = [y[0] for y in Authors]
plt.xticks(range(len(Authors)), cathegorie)
barlist[0].set_color('g')




###Second query
stop = set(stopwords.words('english'))
wordsDict = {}

#select all the lyrics from the mongoDB database
lyrics = db.lyrics.find( {},{ '_id':0, 'lyric': 1 } )
#put all the lyrics in a list
lyricsl = []
for i in lyrics:
    lyricsl.append(i['lyric'])
    
#for every song lyric
for i in lyricsl:
    # removing all the stopwords from the lyric i
    iNoStop = i
    for i in stop:
        lyricList = iNoStop.split()
        for e in range(len(lyricList)):
            if(i.lower() == lyricList[e].lower()): 
                lyricList[e] = ''
                            
        iNoStop = ' '.join(lyricList)
    
    #updating the dictionary containing all the words
    for p in iNoStop.split():
        if(p.lower().strip() in wordsDict.keys()):
            wordsDict[p.lower()] += 1
        else:
            wordsDict[p.lower()] = 1
                        

# this return the 20 most popular words (exclude stopwords)
first20 = sorted(wordsDict.items(), key = operator.itemgetter(1), reverse = True)[:20]

# this is the  histogram of the number of occurence per word for the 20 most popular words
values2 = [x[1] for x in first20]
fig=figure(figsize=(20,10))
barlist2 = plt.bar(range(len(first20)),values2, color = 'c')
cathegorie2 = [y[0] for y in first20]
plt.xticks(range(len(first20)), cathegorie2)
barlist[0].set_color('g')



###third query
NamesDict={}
for author,number in AuthorDict.items():
    name = author.split(' ', 1)[0]
    if name in NamesDict:
        NamesDict[name] += number
    else:
        NamesDict[name] = number
first10 = sorted(NamesDict.items(), key = operator.itemgetter(1), reverse = True)[:10]
#I need to confront it 

###fourth query
#select all the lyrics and titles from the mongoDB database
titlyr = db.lyrics.find( {},{ '_id':0, 'lyric': 1, 'title':1 } )
#create a dictionary with key:title and value:length of the song
lengthsDict = {} #length of the song counting repetitions
for doc in titlyr:
    lengthsDict[doc['title']]=len(doc['lyric'])
#histogramof the song lengths
Songs = sorted(lengthsDict.items(), key = operator.itemgetter(1), reverse = True)
values4 = [x[1] for x in Songs]
fig=figure(figsize=(20,10))
barlist4 = plt.bar(range(len(Songs)),values4, color = 'c', width = 1)
cathegorie4 = [y[0] for y in Songs]
plt.xticks(range(len(Songs)), cathegorie4)
barlist4[0].set_color('g')

#create a dictionary with key:title and value:length of the song
lengthsDict2 = {} #length of the song without counting repetitions
for doc in titlyr:
    lengthsDict2[doc['title']]=len(set(doc['lyric']))
#histogramof the song lengths
Songs2 = sorted(lengthsDict2.items(), key = operator.itemgetter(1), reverse = True)
values5 = [x[1] for x in Songs2]
fig=figure(figsize=(20,10))
barlist5 = plt.bar(range(len(Songs2)),values5, color = 'c', width = 1)
cathegorie5 = [y[0] for y in Songs2]
plt.xticks(range(len(Songs)), cathegorie5)
barlist5[0].set_color('g')


