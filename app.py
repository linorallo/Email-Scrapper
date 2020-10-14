import persistence
import requests, json
import credentials
import phonenumberextractor
# places_query='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key='+credentials.get_google_key()+'&input='

def explore_website(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    soup=str(soup)
    results = [extract(soup)]
    extractor = PhoneNumberExtractor()
    matches = extractor.extract_phone_numbers(soup)
    phones = ', '.join(matches)
    results.append(phones)
    print(results)
    persistence.writeResults(url,results)

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
                    for i in results:
                        obtained_places.append(i)
                except Exception:
                    continue
                break
    print('---')
    return obtained_places


def get_coordinates(city):
    country = 'US'
    state = 'NY'
    query = 'http://dev.virtualearth.net/REST/v1/Locations/'+country+'/'+state+'/' + \
        str(city)+'?o=json&key='+credentials.get_bing_key()
    obtained_resources = []
    result = requests.get(query).json()
    #print(result['resourceSets'][0]['resources'])
    for i in result['resourceSets'][0]['resources']:
        obtained_resources.append(i)
    persistence.save_coordinates(obtained_resources)
    obtained_coordinates=[]
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
    persistence.save_results(businesses_data)

get_data('restaurants')