from services import WeatherApi


if __name__ == '__main__':
    api = WeatherApi()
    api.get_weather(56.6340, 47.8910)
