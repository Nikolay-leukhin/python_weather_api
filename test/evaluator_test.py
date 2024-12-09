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
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_mixed_conditions(self):
        weather = WeatherModel(temp=5, humidity=10, wind_speed=45, rain_prob=50)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_edge_case_high_rain(self):
        weather = WeatherModel(temp=20, humidity=50, wind_speed=20, rain_prob=95)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_edge_case_low_rain(self):
        weather = WeatherModel(temp=20, humidity=50, wind_speed=20, rain_prob=39)
        self.assertFalse(Evaluator.is_bad_weather(weather))

    def test_extremely_hot_weather(self):
        weather = WeatherModel(temp=45, humidity=30, wind_speed=10, rain_prob=5)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_extremely_cold_weather(self):
        weather = WeatherModel(temp=-25, humidity=50, wind_speed=10, rain_prob=10)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_high_wind_speed(self):
        weather = WeatherModel(temp=20, humidity=50, wind_speed=70, rain_prob=10)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_high_humidity_and_high_temp(self):
        weather = WeatherModel(temp=38, humidity=95, wind_speed=10, rain_prob=10)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_high_humidity_and_low_temp(self):
        weather = WeatherModel(temp=0, humidity=95, wind_speed=10, rain_prob=10)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_extreme_conditions_combined(self):
        weather = WeatherModel(temp=40, humidity=100, wind_speed=60, rain_prob=80)
        self.assertTrue(Evaluator.is_bad_weather(weather))

    def test_moderate_conditions_with_high_rain(self):
        weather = WeatherModel(temp=25, humidity=50, wind_speed=20, rain_prob=75)
        self.assertTrue(Evaluator.is_bad_weather(weather))


if __name__ == '__main__':
    unittest.main()



