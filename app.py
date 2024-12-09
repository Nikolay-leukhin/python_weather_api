from flask import Flask, render_template, request
from models import WeatherModel
from services import Evaluator, WeatherApi
from errors import LocationNotFoundError

app = Flask(__name__)
api = WeatherApi()

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@app.route('/eval', methods=['POST'])
def evaluate():
    start_point = request.form['start_point']
    end_point = request.form['end_point']

    try:
        start_weather = api.get_weather_by_city_name(start_point)
        end_weather = api.get_weather_by_city_name(end_point)

        result = "Плохие погодные условия" if Evaluator.eval_weather_list(
            data=start_weather + end_weather) else "Хорошие погодные условия"

        return render_template('result.html', result=result)
    except LocationNotFoundError as ex:
        return render_template('result.html', result="location not found")
    except Exception as ex:
        print(ex)
        return render_template('result.html', result="unpredictable exception")


if __name__ == '__main__':
    app.run(debug=True)
