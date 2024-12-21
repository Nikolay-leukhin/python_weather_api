import requests
import json

from errors import LocationNotFoundError, BadWeatherResponse
from models import WeatherModel


class WeatherApi:
    __API_KEY = 'wUMIOqbn2qPjvQqCkBAGgJyLPP0No13E'
    __API_CITY_KEY = '73e3d50183089ceebacb8c4a36fe94c3'
    __BASE_URL = 'http://dataservice.accuweather.com/'

    def get_weather(self, lat, lon):
        location = self.get_location_by_cords(lat, lon)
        url = f"{self.__BASE_URL}currentconditions/v1/{location}"
        params = {
            'apikey': self.__API_KEY,
            'details': True,
            'language': 'ru-ru'
        }

        weather_response = requests.get(url, params=params)

        if weather_response.status_code != 200:
            raise BadWeatherResponse(weather_response.text)

        return [WeatherModel.from_json(item, city='none', day=1, lat=lat, lon=lon) for item in weather_response.json()]

    def get_weather_by_city_name(self, city, days):
        city = city.strip()
        location = self.get_location_by_city(city)
        url = f"{self.__BASE_URL}forecasts/v1/daily/5day/{location}"
        params = {
            'apikey': self.__API_KEY,
            'details': True,
            'language': 'ru-ru',
            'metric': True
        }

        weather_response = requests.get(url, params=params)
        if weather_response.status_code != 200:
            raise BadWeatherResponse(weather_response.text)

        lat, lon = self.get_city_coordinates(city, self.__API_CITY_KEY)
        result = [WeatherModel.from_json(item, city=city, day=ind, lat=lat, lon=lon) for ind, item in enumerate(weather_response.json()['DailyForecasts'])]
        return result

    def get_location_by_cords(self, lat, lon):
        location_url = self.__BASE_URL + 'locations/v1/cities/geoposition/search'
        params = {
            'q': f"{lat},{lon}",
            'apikey': self.__API_KEY
        }

        response_location = requests.get(location_url, params=params)
        location_key = response_location.json().get('Key', None)

        if location_key is None:
            raise LocationNotFoundError()

        return location_key

    def get_location_by_city(self, city):
        url = self.__BASE_URL + f'locations/v1/cities/search'
        params = {
            'apikey': self.__API_KEY,
            'q': city
        }

        response_location = requests.get(url, params=params)
        if len(response_location.json()) == 0:
            raise LocationNotFoundError()

        location_key = response_location.json()[0].get('Key', None)

        if location_key is None:
            raise LocationNotFoundError()

        return location_key

    def get_city_coordinates(self, city_name, api_key):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'coord' in data:
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                return lat, lon
            else:
                raise ValueError(f"Could not find coordinates for city: {city_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching data: {e}")
            raise


if __name__ == '__main__':
    api = WeatherApi()
    print(api.get_weather_by_city_name('Moscow', 5))

