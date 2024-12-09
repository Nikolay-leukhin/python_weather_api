import requests
import json

from errors import LocationNotFoundError, BadWeatherResponse
from models import WeatherModel


class WeatherApi:
    __API_KEY = 'HxpvXQpFDc1lyb3zgnwA6gw7r40YlR2G'
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

        return [WeatherModel.from_json(item) for item in weather_response.json()]

    def get_weather_by_city_name(self, city):
        city = city.strip()
        location = self.get_location_by_city(city)
        url = f"{self.__BASE_URL}currentconditions/v1/{location}"
        params = {
            'apikey': self.__API_KEY,
            'details': True,
            'language': 'ru-ru'
        }

        weather_response = requests.get(url, params=params)

        if weather_response.status_code != 200:
            raise BadWeatherResponse(weather_response.text)

        return [WeatherModel.from_json(item) for item in weather_response.json()]

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


if __name__ == '__main__':
    api = WeatherApi()
    print(api.get_weather(52, 46))

