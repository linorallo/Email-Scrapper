import persistence
import requests, json
import credentials
# places_query='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key='+credentials.get_google_key()+'&input='


def get_locations(business, locations):
    query = 'https://dev.virtualearth.net/REST/v1/LocalSearch/?query=' + \
        business+'&maxResults=25'
    offset = 0.02
    obtained_places = []
    for location in locations:
        responses_obtained = []
        for i in range(1):
            location
        coordinates = str(location['coordinates'][0])+','+str(location['coordinates'][1])
        responses = requests.get(query+'&userLocation='+coordinates+'&key='+credentials.get_bing_key()).json()
        results = responses['resourceSets'][0]['resources']
        for i in results:
            responses_obtained.append(i)
        print(str(len(results)) + ' results obtained in ' + location['name'])
        obtained_places.append(responses_obtained)
    print(str(len(obtained_places)) + ' businesses obtained')
    return obtained_places


def get_coordinates(city):
    country = 'US'
    state = 'NY'
    query = 'http://dev.virtualearth.net/REST/v1/Locations/'+country+'/'+state+'/' + \
        str(city)+'?o=json&key='+credentials.get_bing_key()
    obtained_resources = []
    result = requests.get(query).json()
    for i in result['resourceSets'][0]['resources']:
        obtained_resources.append(i)
    persistence.save_results(obtained_resources)
    obtained_coordinates=[]
    for i in obtained_resources:
        coordinates = dict(name = i['address']['locality'], coordinates = i['point']['coordinates'])
        obtained_coordinates.append(coordinates)
    print(obtained_coordinates)
    return obtained_coordinates


def get_cities():
    cities = persistence.read_cities()
    return cities


def get_businesses(business):
    all_cities = get_cities()
    cities = []
    for i in all_cities:
        if len(i)>0:
            print(i)
            i.split(',')
            city_status = i.split(',')[1]
            if city_status != 'Checked':
                cities.append(i.split(',')[0])
    locations = get_coordinates(cities)
    businesses_data = get_locations(business, locations)
    persistence.save_results(businesses_data)

