from datetime import datetime
import credentials


def readURL():
    urls = open('url_list.txt', 'r').read()
    urls = str(urls).split('\n')
    return urls


def writeResults(url, results):
    f = open(str(datetime.now())+'.txt', "w+")
    f.write(url+'\n')
    for i in results:
        f.write(str(i)+'\n')
    f.close()

def read_cities():
    urls = open('cities_list.csv', 'r').read()
    urls = str(urls).split('\n')
    return urls

def save_results(results):
    f = open('results/businesses/'+str(datetime.now())+'.txt', "w+")
    for i in results:
        f.write(str(i)+'\n')
    f.close()

def save_coordinates(results):
    f = open('results/coordinates/'+str(datetime.now())+'.txt', "w+")
    f.write('----------------------'+'\n')
    for i in results:
        f.write(str(i)+'\n')
    f.close()