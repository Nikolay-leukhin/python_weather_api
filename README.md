Weather project

All of these features you can try in test directory

Functionality:

1. Weather Api 
requests Accuweather about current weather in participate place by lat and lon. 
/test/weather_api_test.py

-Added DTO WeatherModel about main aspects of the weather

2. Evaluator
mini model that tries to evaluate the weather and provides is the weather is favorable
also you can always test the model in /test/evaluator_test.py. there are unit test that can help the test the model

3. I set validator on form to get rid of exceptions main exception about that you cannot found the place and other
also I handle the location not found exception and the grouped the exceptions with no internet connection or exceptions on server side in group Unpredictable exception

