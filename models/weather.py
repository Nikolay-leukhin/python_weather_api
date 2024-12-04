from typing import Dict, Any


class WeatherModel:
    def __init__(self, temp: float, humidity: float, wind_speed: float, rain_prob: float):
        self.temp = temp
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.rain_prob = rain_prob

    def to_json(self) -> Dict[str, Any]:
        return {
            'temperature': self.temp,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'precipitation_probability': self.rain_prob
        }

    @classmethod
    def from_json(cls, data: Dict):
        return WeatherModel(
            temp=data['Temperature']['Metric']['Value'],
            humidity=data['RelativeHumidity'],
            wind_speed=data['Wind']['Speed']['Metric']['Value'],
            rain_prob=data['HasPrecipitation'] * 100
        )

    def __repr__(self) -> str:
        return (f"WeatherModel(temperature={self.temp}°C, "
                f"humidity={self.humidity}%, "
                f"wind_speed={self.wind_speed} km/h, "
                f"precipitation_probability={self.rain_prob}%)")
