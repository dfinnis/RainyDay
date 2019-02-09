import requests
import json
import pandas as pd

# LOCATIONS: ORIGIN - DESTINATION

depart = input('Origin: ')
destination = input('Destination: ')
print('')

url_key_dept = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=yIogKOV20SikvJe2zKQylcw5sA266KqC&q={}'.format(depart)
res_key_dept = requests.get(url_key_dept)
data_key_dept = res_key_dept.json()
try:
    key_dept = data_key_dept[0]['Key']
except:
    print('Invalid city name, or API request limit exceeded')
    exit(0)
lat_1 = data_key_dept[0]['GeoPosition']['Latitude']
long_1 = data_key_dept[0]['GeoPosition']['Longitude']

url_key_dest = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=yIogKOV20SikvJe2zKQylcw5sA266KqC&q={}'.format(destination)
res_key_dest = requests.get(url_key_dest)
data_key_dest = res_key_dest.json()
try:
    key_dest = data_key_dest[0]['Key']
except:
    print('Invalid city name, or API request limit exceeded')
    exit(0)
lat_2 = data_key_dest[0]['GeoPosition']['Latitude']
long_2 = data_key_dest[0]['GeoPosition']['Longitude']

# ROUTE

url_map = 'http://www.yournavigation.org/api/1.0/gosmore.php?format=geojson&flat={0}&flon={1}&tlat={2}&tlon={3}&v=bicycle&fast=1&layer=mapnik'.format(lat_1, long_1, lat_2, long_2)
res_route = requests.get(url_map)
try:
    data_route = res_route.json()
except:
    print('hmmm are you trying to cycle across the sea??')
    exit(0)
traveltime = data_route['properties']['traveltime']
traveltime = int(traveltime) / 3600
traveltime_hours = int(traveltime)
if traveltime == 0 :
    print("hmmm are you trying to cycle across the sea?")
    exit(0)
if traveltime_hours > 12 :
    print("You ain't making it there today")
    exit(0)

stops = traveltime_hours - 2
stops_list = []

if stops > 0:
    coordinates = data_route['coordinates']
    num_coordinates = len(coordinates)    
    sections = num_coordinates / traveltime_hours
    for stop in range(stops):
        index = int(sections) * (stop + 1)
        longitude = data_route['coordinates'][index][0]
        latitude = data_route['coordinates'][index][1]
        url_city = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=yIogKOV20SikvJe2zKQylcw5sA266KqC&q={0}%2C{1}'.format(latitude, longitude)
        res_city = requests.get(url_city)
        data_city = res_city.json()
        city = dict.fromkeys({'city', 'key'})
        try:
            city['city'] = data_city['LocalizedName']
        except:
            print('API request limit exceeded')
            exit(0)
        city['key'] = data_city['Key']
        stops_list.append(city)

# WEATHER

all_stops = []

def fahr_to_celsius(temp):
    return(int((temp - 32) * (5/9)))

# WEATHER DEPART

loc = dict.fromkeys({'Location', ' % Chance of Rain', ' Temperature'})
url_dept = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{}?apikey=yIogKOV20SikvJe2zKQylcw5sA266KqC'.format(key_dept)
res_dept = requests.get(url_dept)
data_dept = res_dept.json()
loc['Location'] = depart
try:
    loc[' % Chance of Rain'] = data_dept[0]['PrecipitationProbability']
except:
    loc[' % Chance of Rain'] = 0
try:
    loc[' Temperature'] = fahr_to_celsius(data_dept[0]['Temperature']['Value'])
except:
    print('API request limit exceeded')
    exit(0)
all_stops.append(loc)

# WEATHER STOPS

if stops > 0:
    for stop in range(stops):
        loc = dict.fromkeys({'Location', ' % Chance of Rain', ' Temperature'})
        key = stops_list[stop]['key']
        url_stop = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{}?apikey=yIogKOV20SikvJe2zKQylcw5sA266KqC'.format(key)
        res_stop = requests.get(url_stop)
        data_stop = res_stop.json()
        try:
            loc['Location'] = stops_list[stop]['city']
        except:
            print('API request limit exceeded')
            exit(0)
        try:
            loc[' % Chance of Rain'] = data_stop[stop]['PrecipitationProbability']
        except:
            loc[' % Chance of Rain'] = 0
        loc[' Temperature'] = fahr_to_celsius(data_stop[stop]['Temperature']['Value'])
        all_stops.append(loc)

# WEATHER DESTINATION

loc = dict.fromkeys({'Location', '% Chance of Rain', ' Temperature'})
url_dest = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{}?apikey=yIogKOV20SikvJe2zKQylcw5sA266KqC'.format(key_dest)
res_dest = requests.get(url_dest)
data_dest = res_dest.json()
loc['Location'] = destination
try:
    loc[' % Chance of Rain'] = data_dest[traveltime_hours]['PrecipitationProbability']
except:
    loc[' % Chance of Rain'] = 0
try:
    loc[' Temperature'] = fahr_to_celsius(data_dest[traveltime_hours]['Temperature']['Value'])
except:
    print('API request limit exceeded')
    exit(0)
all_stops.append(loc)

# DISPLAY RESULTS

all_stops = pd.DataFrame(all_stops, columns=['Location', ' % Chance of Rain', ' Temperature'])
print(all_stops)