from models import WeatherModel


class Evaluator:
    @classmethod
    def is_bad_weather(cls, weather: WeatherModel) -> bool:
        score = 0
        if weather.temp < -24:
            score += 3
        elif weather.temp < -10:
            score += 2
        elif weather.temp > 35:
            score += 3

        if weather.wind_speed > 50:
            score += 4
        elif weather.wind_speed > 30:
            score += 3

        if weather.rain_prob > 70:
            score += 3
        elif weather.rain_prob > 40:
            score += 1

        if weather.humidity > 92:
            score += 3
        elif weather.humidity > 80:
            score += 2
        elif weather.humidity < 20:
            score += 2
        return score >= 3

    @staticmethod
    def eval_weather_list(data: list[WeatherModel]):
        return any([Evaluator.is_bad_weather(item) for item in data])
