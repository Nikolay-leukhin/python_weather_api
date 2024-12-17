from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import send_from_directory
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from models import WeatherModel
from services import Evaluator, WeatherApi
from errors import LocationNotFoundError

app = Flask(__name__)
api = WeatherApi()

dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')

dash_app.layout = html.Div([
    html.H1("Визуализация погодных данных"),
    dcc.Dropdown(
        id='parameter-dropdown',
        options=[
            {'label': 'Температура', 'value': 'temperature'},
            {'label': 'Скорость ветра', 'value': 'wind_speed'},
            {'label': 'Вероятность осадков', 'value': 'precipitation'}
        ],
        value='temperature',
        placeholder="Выберите параметр"
    ),
    dcc.Graph(id='weather-graph')
])


@dash_app.callback(
    Output('weather-graph', 'figure'),
    [Input('parameter-dropdown', 'value')]
)
def update_graph(selected_param):
    data = {
        "city": ["Город A", "Город B", "Город C"],
        "temperature": [15, 20, 25],
        "wind_speed": [5, 10, 15],
        "precipitation": [0.2, 0.4, 0.1]
    }
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="city",
        y=selected_param,
        title=f"График по параметру: {selected_param.capitalize()}",
        labels={"city": "Город", selected_param: "Значение"}
    )
    return fig


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


@app.route('/visualization', methods=['GET'])
def visualization():
    return redirect('/dash/')


if __name__ == '__main__':
    app.run(debug=True)
