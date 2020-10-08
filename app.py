import persistence
import requests, json
import credentials
# places_query='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key='+credentials.get_google_key()+'&input='


def get_locations(business, locations):
    query = 'https://dev.virtualearth.net/REST/v1/LocalSearch/?query=' + \
        business+'&maxResults=25'
    try:
        obtained_places = []
        for location in locations:
            obtained_places.append(requests.get(
                places_query+'&userLocation='+coordinates+'&key='+credentials.get_bing_key()))
        return obtained_places
    except expression as identifier:
        pass


def get_coordinates(city):
    country = 'US'
    state = 'NY'
    query = 'http://dev.virtualearth.net/REST/v1/Locations/'+country+'/'+state+'/' + \
        str(city)+'?o=json&key='+credentials.get_bing_key()
    obtained_resources = []
    #for coordinates in requests.get(query):
        #result = json.loads(coordinates)
    result = requests.get(query).json()
    print(result['resourceSets'][0]['resources'])
    for i in result['resourceSets'][0]['resources']:
        obtained_resources.append(i)
    persistence.save_results(obtained_resources)
    obtained_coordinates=[]
    for i in obtained_coordinates:
        coordinates = dict(name = i['name'], coordinates = i['point']['coordinates'])
        print(coordinates)
        obtained_coordinates.append(coordinates)
    return obtained_coordinates


def get_cities():
    cities = persistence.read_cities()
    return cities


def get_businesses(business):
    cities = get_cities()
    locations = get_coordinates(cities)
    businesses_data = get_locations(business, locations)
    persistence.save_results(businesses_data)
