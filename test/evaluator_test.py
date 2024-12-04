import unittest
from models import WeatherModel
from services import Evaluator


class TestEvaluator(unittest.TestCase):
    def test_cold_but_not_bad(self):
        weather = WeatherModel(temp=-1, humidity=50, wind_speed=20, rain_prob=10)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_hot_but_not_bad(self):
        weather = WeatherModel(temp=34, humidity=50, wind_speed=20, rain_prob=10)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_high_wind_but_not_bad(self):
        weather = WeatherModel(temp=25, humidity=50, wind_speed=49, rain_prob=10)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_moderate_rain(self):
        weather = WeatherModel(temp=20, humidity=50, wind_speed=20, rain_prob=40)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_high_humidity_but_not_bad(self):
        weather = WeatherModel(temp=25, humidity=89, wind_speed=20, rain_prob=10)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_low_humidity_but_not_bad(self):
        weather = WeatherModel(temp=25, humidity=19, wind_speed=20, rain_prob=10)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_high_wind_with_low_temp(self):
        weather = WeatherModel(temp=-5, humidity=50, wind_speed=55, rain_prob=10)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_mixed_conditions(self):
        weather = WeatherModel(temp=5, humidity=10, wind_speed=45, rain_prob=50)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_edge_case_high_rain(self):
        weather = WeatherModel(temp=20, humidity=50, wind_speed=20, rain_prob=95)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_edge_case_low_rain(self):
        weather = WeatherModel(temp=20, humidity=50, wind_speed=20, rain_prob=39)
        self.assertFalse(Evaluator.is_bad_weather(weather))


if __name__ == '__main__':
    unittest.main()

