import requests

def get_weather_data(city):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'units': 'metric',
        'appid': settings.OPENWEATHER_API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None