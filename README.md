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

----------------
Project 3 comments

1. I chose bar charts to show weather data for a specific day because they make it easy to compare different things, like temperature, humidity, and wind speed. Line charts are good for showing how these weather aspects change over time. This helps users see trends and changes in the weather during the day or week.
2. Interactive charts help users get information from the website faster. They can click on different parts of the chart to see more details. This makes websites more user-friendly because users can find the information they need easily and understand the data better. It also makes the experience

