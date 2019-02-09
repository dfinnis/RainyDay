import requests
import json

# LOCATIONS: DEPARTURE + DESTINATION

depart = input('Depart: ')
destination = input('Destination: ')

url_key_dept = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=U7hpXKPf7PlbYOPeTaGPT5GGU8tN9MJH&q={}'.format(depart)
res_key_dept = requests.get(url_key_dept)

data_key_dept = res_key_dept.json()
key_dept = data_key_dept[0]['Key']
lat_1 = data_key_dept[0]['GeoPosition']['Latitude']
long_1 = data_key_dept[0]['GeoPosition']['Longitude']

url_key_dest = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=U7hpXKPf7PlbYOPeTaGPT5GGU8tN9MJH&q={}'.format(destination)
res_key_dest = requests.get(url_key_dest)

data_key_dest = res_key_dest.json()
key_dest = data_key_dest[0]['Key']
lat_2 = data_key_dest[0]['GeoPosition']['Latitude']
long_2 = data_key_dest[0]['GeoPosition']['Longitude']

# ROUTE

url_map = 'http://www.yournavigation.org/api/1.0/gosmore.php?format=geojson&flat={0}&flon={1}&tlat={2}&tlon={3}&v=bicycle&fast=1&layer=mapnik'.format(lat_1, long_1, lat_2, long_2)
res_route = requests.get(url_map)
data_route = res_route.json()
#print(data_route)



traveltime = data_route['properties']['traveltime']
traveltime = int(traveltime) / 3600
traveltime_hours = int(traveltime)

stops = traveltime_hours - 2
stops_list = []
print(stops)

if stops > 0:
    coordinates = data_route['coordinates']
    num_coordinates = len(coordinates)    
    sections = num_coordinates / traveltime_hours
    for stop in range(stops):
        index = int(sections) * (stop + 1)
        latitude = data_route['coordinates'][index][0]
        longitude = data_route['coordinates'][index][1]
        url_city = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=%09U7hpXKPf7PlbYOPeTaGPT5GGU8tN9MJH&q={}%2C{}'.format(latitude, longitude)
        res_city = requests.get(url_city)
        #print(res_city)
        data_city = res_city.json()
        print(type(data_city))
        #name = data_city['LocalizedName']
        #key = data_city['Key']
        #city = [name, key]
        #stops_list.append(city)

#print(stops_list)

 #       //find lat and long for (num_coordinates / stops) * stop
  #      //find weather forcast for lat&long at time(stop)

  #  city key by lat lon = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=%09U7hpXKPf7PlbYOPeTaGPT5GGU8tN9MJH&q={}%2C{}'.format(lat, lon)

# STOPS INFO




# WEATHER

#url_dept = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{}?apikey=U7hpXKPf7PlbYOPeTaGPT5GGU8tN9MJH'.format(key_dept)
#res_dept = requests.get(url_dept)
#data_dept = res_dept.json()
#rain_dept = data_dept[0]['PrecipitationProbability']
#temp_dept = data_dept[0]['Temperature']['Value']
#
#
#
#
#
#url_dest = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{}?apikey=U7hpXKPf7PlbYOPeTaGPT5GGU8tN9MJH'.format(key_dest)
#res_dest = requests.get(url_dest)
#data_dest = res_dest.json()
#rain_dest = data_dest[traveltime_hours]['PrecipitationProbability']
#temp_dest = data_dest[traveltime_hours]['Temperature']['Value']
#
#print(depart, rain_dept, temp_dept, "\n")
#print(destination, rain_dest, temp_dest, "\n")


###############

#print(long_1, "\n")
#print(rain, "\n")
#print(rain_time, "\n")
#print(data_dest)

#url_dept = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=334f3fc1cca6476739d85a7ee319f47b'.format(depart)
#url_dest = 'http://api.openweathermap.org/data/2.5/forecast?q={}&APPID=334f3fc1cca6476739d85a7ee319f47b'.format(destination)

#data_dept = res.json()
#data_dest = res.json()

#lat_1 = data_dept['coord']['lat']
#long_1 = data_dept['coord']['lon']
#lat_2 = data_dest['city']['coord']['lat']
#long_2 = data_dest['city']['coord']['lon']

#rain = data_dest['list'][0]['rain']['3h'] # for ___in data_dest, try 'rain'
#rain_time = data_dest['list'][0]['dt_txt']