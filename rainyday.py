import requests

depart = input('Depart from: ')

url = 'http://api.openweathermap.org/data/2.5/forecast?q={}}&APPID=334f3fc1cca6476739d85a7ee319f47b'.format(depart)

res = requests.get(url)

data = res.json()

print(res)

print(data)