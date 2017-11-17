import urllib.request
import csv

# Function to retrieve data from Open Data Portal of the City of Rome
# url: the location of the dataset (in CSV format) in the Open Data Portal
# localfile: the filename that will be used to store the file on the local disk
# header: the initial rows that do not include any data and should be excluded
# footer: the trailing rows that do not include any data and should be excluded
def loadDataRemote(url, localfile, header, footer):
    # connect and retrieve dataset
    u = urllib.request.urlopen(url)
    rawdata = u.read()    
    
    # store on local filesystem
    f = open(localfile, "wb")
    f.write(rawdata)
    f.close()    

    # load and prepare data structure
    return loadDataLocal(localfile, header, footer)

# Function to retrieve data from Open Data Portal of the City of Rome
# localfile: the filename of the dataset in CSV format
# header: the initial rows that do not include any data and should be excluded
# footer: the trailing rows that do not include any data and should be excluded
def loadDataLocal(localfile, header, footer):
    # load CSV data
    f = open(localfile)
    rawdata = []
    for row in csv.reader(f, delimiter=';'):
        rawdata.append(row)    
        
    # exclude header / footer
    dataset = rawdata[header: -footer]
    
    # convert text into number
    for row in dataset:
        for value in range(2, len(row)):
            row[value] = int(row[value].replace('.',''))    
            
    # dataset properly loaded
    return dataset


dataset2014 = loadDataRemote('http://dati.comune.roma.it/cms/do/jacms/Content/incrementDownload.action?contentId=DTS542&filename=popolazione_straniera_iscritta_in_anagrafe_per_municipio_e_sesso_e_cittadinanza_al_31_dicembre_20145ee4.csv',\
                             'rome-2014.csv', 5, 5)
dataset2013 = loadDataRemote('http://dati.comune.roma.it/cms/do/jacms/Content/incrementDownload.action?contentId=DTS725&filename=18-pop_stra_mun_cittad_1310ef.csv',\
                             'rome-2013.csv', 7, 5)
dataset2012 = loadDataRemote('http://dati.comune.roma.it/cms/do/jacms/Content/incrementDownload.action?contentId=DTS728&filename=18-pop_stra_mun_cittad_1292e6.csv',\
                             'rome-2012.csv', 7, 5)

dataset2014 = loadDataLocal('rome-2014.csv', 5, 5)
dataset2013 = loadDataLocal('rome-2013.csv', 7, 5)
dataset2012 = loadDataLocal('rome-2012.csv', 7, 5)

dataset2014.sort(key=lambda x: x[len(x)-1], reverse=True)
dataset2013.sort(key=lambda x: x[len(x)-1], reverse=True)
dataset2012.sort(key=lambda x: x[len(x)-1], reverse=True)


#Reference link for data visualization
#https://github.com/ichatz/adm/blob/master/lab-visualization/ADM%20Lab%20-%20Visualization.ipynb

#using MatPlot lib
values = []
for x in range(0, 15):
    values.append(dataset2014[0][4+x*3])

import matplotlib.pyplot as plt
plt.plot(values)
plt.show()


#For verifying the current working directory
import os
print(os.getcwd())

#For creating mongo db documents from data from a json file

