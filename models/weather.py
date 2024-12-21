from typing import Dict, Any


class WeatherModel:
    def __init__(self, temp: float, humidity: float, wind_speed: float, rain_prob: float, city: str, day: int, lat: float, lon: float):
        self.temp = temp
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.rain_prob = rain_prob
        self.city = city
        self.day = day
        self.lat = lat
        self.lon = lon

    def to_json(self) -> Dict[str, Any]:
        return {
            "city": self.city,
            "day": self.day,
            "temperature": self.temp,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "precipitation_probability": self.rain_prob,
            "lat": self.lat,
            "lon": self.lon
        }

    @classmethod
    def from_json(cls, data: Dict, city: str, day: int, lat: float, lon: float):
        return WeatherModel(
            temp=round((data['Temperature']['Minimum']['Value'] + data['Temperature']['Maximum']['Value']) / 2, 2),
            humidity=data['Day']['RelativeHumidity']['Average'],
            wind_speed=data['Day']['Wind']['Speed']['Value'],
            rain_prob=data['Day']['PrecipitationProbability'],
            city=city,
            day=day,
            lon=lon,
            lat=lat
        )

    def __repr__(self) -> str:
        return (f"WeatherModel(temperature={self.temp}°C, "
                f"humidity={self.humidity}%, "
                f"wind_speed={self.wind_speed} km/h, "
                f"precipitation_probability={self.rain_prob}%), city:{self.city}, day:{self.day}")
