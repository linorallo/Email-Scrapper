import persistence
import requests, json
import credentials
from phonenumberextractor import PhoneNumberExtractor
from html_analizer import extract
from bs4 import BeautifulSoup
import time
# places_query='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key='+credentials.get_google_key()+'&input='

def extract_data_from_website(url, prefix):
    i= 0 
    while True:
        try:
            if '.com' in str(url):
                print('Attempting extraction to:')
                print(url)
                response=requests.get(url)
                break
            else:
                if len(prefix)>2:
                    print(prefix[len(prefix)-1])
                    if url[0] != '/':
                        
                        if prefix[len(prefix)-1] != '/':
                            url = prefix+'/'+url
                        else:
                            url = prefix + url
                    else:
                        if prefix[len(prefix)-1] == '/':
                            url = prefix+url[1:len(url)]
                        else:
                            url = prefix+url
                    response = requests.get(url)
                    break
                i=10
            raise Exception
        except Exception as err:
            print(err)
            i+=1
            print(i)
            time.sleep(5)
            if i >= 5:
                print('5th attempt skipping')
                response = 'bad'
                break
    if response != 'bad':
        soup=BeautifulSoup(response.text,'html.parser')
        soup=str(soup)
        results = [extract(soup)]
        extractor = PhoneNumberExtractor()
        matches = extractor.extract_phone_numbers(soup)
        phones = ', '.join(matches)
        results.append(phones)
        print(results)
        persistence.save(results,'contact_data')

def explore_website(url):
    while True:
        try:
            response=requests.get(url)
            break
        except Exception as err:
            print(err)
            continue
    extract_data_from_website(url,'')
    soup=BeautifulSoup(response.text,'html.parser')
    result_url = []
    for link in soup.findAll(href=True):
        try:
            href = str(link['href'])
            if 'contact' in str(href):
                result_url.append(href)
        except TypeError :
            continue
    purged_elements = set()
    for elem in result_url:
        if elem  not in purged_elements:
                purged_elements.add(elem)
                print(elem)
                extract_data_from_website(elem,url)
    persistence.save_links(purged_elements)
    #persistence.purge_links()

def get_businesses(business, locations):
    query = 'https://dev.virtualearth.net/REST/v1/LocalSearch/?query=' + \
        business+'&maxResults=25'
    obtained_places = []
    for location in locations:
        for coordinates in location['coordinates']:
            print(coordinates)
            while True:
                try:
                    results = requests.get(query+'&userLocation='+str(coordinates[0])+','+str(coordinates[1])+'&key='+credentials.get_bing_key()).json()['resourceSets'][0]['resources']
                    print(results)
                    for i in results:
                        obtained_places.append(i)
                        website = i['Website'] 
                        if str(website) != 'None':
                            explore_website(website)
                except Exception as err:
                    print(err)
                    continue
                break
    return obtained_places


def get_coordinates(cities):
    country = 'US'
    state = 'NY'
    obtained_resources = []

    existing_cities = persistence.bulk_read('coordinates')
    new_cities = set()
    for city in cities:
        for i in existing_cities:
            print(i['name'].split(',')[0])
            print(city)
            print('------------')
            if i['name'].split(',')[0] != city:
                new_cities.add(city)
        if len(existing_cities) == 0:
            new_cities.add(city)
    obtained_coordinates=[]
    print('new cities')
    print(new_cities)

    for city in new_cities:
        query = 'http://dev.virtualearth.net/REST/v1/Locations/'+country+'/'+state+'/' + \
        str(city)+'?o=json&key='+credentials.get_bing_key()
        while True:
            try:
                result = requests.get(query).json()
                break
            except Exception:
                continue
        for i in result['resourceSets'][0]['resources']:
            obtained_resources.append(i)
        persistence.save(obtained_resources,'coordinates')
        offset = 0.02
        for i in obtained_resources:
            original_coordinates = i['point']['coordinates']
            quadrant_1 = [original_coordinates[0] + offset, original_coordinates[1] - offset]
            quadrant_2 = [original_coordinates[0] - offset, original_coordinates[1] + offset]
            quadrant_3 = [original_coordinates[0] - offset, original_coordinates[1] - offset]
            quadrant_4 = [original_coordinates[0] + offset, original_coordinates[1] + offset]
            coordinates  = [original_coordinates,quadrant_1,quadrant_2,quadrant_3,quadrant_4]
            all_coordinates = dict(name = i['name'], coordinates = coordinates)
            obtained_coordinates.append(all_coordinates)
    return obtained_coordinates

def get_cities():
    cities = persistence.read_cities()
    return cities

def get_data(business):
    cities = get_cities()
    locations = get_coordinates(cities)
    businesses_data = get_businesses(business, locations)
    persistence.save(businesses_data, 'business')

get_data('restaurants')
#get_coordinates(['East Patchogue'])