from datetime import datetime
import credentials
import glob
import os, json, ast

def purge_duplicates(all_elements, type):
    purged_elements = set()
    for elem in all_elements:
        if elem  not in purged_elements:
            purged_elements.add(elem)
    if type == 'links':
        bulk_delete('links')
        save_links(purged_elements)
    elif type == 'contact_data':
        bulk_delete('contact_data')
        save(purged_elements, 'contact_data')
    else:
        return
        
def purge_links():
    purge_duplicates(bulk_read('links'), 'links')

def purge_contact_data():
    purge_duplicates(bulk_read('contact_data'), 'contact-data')

def bulk_read(option):
    if option == 'contact_data':
        directory = 'results/businesses/contact_data/*.txt'
    if option == 'links':
        directory = 'results/businesses/links/*.txt'
    if option == 'coordinates':
        directory = 'results/coordinates/*.txt'
    if option == 'api':
        directory = 'results/businesses/api/websites.csv'
    files = glob.glob(directory)
    data = []
    for i in files:
        row = open(i, 'r').read().split('\n')
        if len(str(row))>3:
            if (option == 'api') or (option == 'contact_data') or (option == 'links'):
                data.append(row)
            else:
                for j in row:
                    k = j
                    j  = j.rstrip()
                    k = str(j).replace('\'','\"')
                    print(k)
                    j = json.loads(k)
                    data.append(j)
    return data

def bulk_delete(option):
    if option == 'contact_data':
        directory = 'results/businesses/contact_data/*.txt'
    if option == 'links':
        directory = 'results/businesses/links/*.txt'
    if option == 'coordinates':
        directory = 'results/coordinates/*.txt'
    files = glob.glob(directory)
    for i in files:
        os.remove(i)

def save_links(links):
    f = open('results/businesses/links/'+str(datetime.now().timestamp())+'.txt', "w+")
    for i in links:
        if len(str(i))>3:
            f.write(str(i)+'\n')
    f.close()

def read_cities():
    urls = open('cities_list.csv', 'r').read()
    urls = str(urls).split('\n')
    return urls

def save(data, option):
    if option == 'contact_data':
        directory = 'results/businesses/contact_data/'
    if option == 'links':
        directory = 'results/businesses/links/'
    if option == 'business':
        directory = 'results/businesses/api/'
    if option == 'coordinates':
        directory = 'results/coordinates/'
    f = open(directory + str(datetime.now().timestamp()) + '.txt', "w+")
    count = 0
    for i in data:
        count+=1
        if (len(data)-count)==0:
            f.write(str(i))
            break
        f.write(str(i)+'\n')
    f.close()