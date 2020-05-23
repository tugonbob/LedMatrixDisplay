import requests

def get_temp(city):
    res = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid=f65e0201135c72e90460f1515e6c4bdb&units=metric'.format(city))
    data = res.json()
    temp = round( data['main']['temp'] )
    return str(temp) + "\"C"    #   '"' is my discount degree symbol

def get_weather(city):
    res = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid=f65e0201135c72e90460f1515e6c4bdb&units=metric'.format(city))
    data = res.json()
    weather = data['weather'][0]['description']
    return str(weather)

