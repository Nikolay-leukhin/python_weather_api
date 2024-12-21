from flask import Flask, render_template, request, redirect, url_for
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from services import WeatherApi
from errors import LocationNotFoundError

app = Flask(__name__)
api = WeatherApi()

data = []
days = 1

dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

dash_app.layout = html.Div([
    html.H1("Weather Data Visualization"),
    dcc.Tabs(id='tabs', value='graph', children=[
        dcc.Tab(label='Графики', value='graph'),
        dcc.Tab(label='Карта маршрута', value='map'),
    ]),
    html.Div(id='content')
])


@dash_app.callback(
    Output('content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'graph':
        return html.Div([
            dcc.Dropdown(
                id='metric-selector',
                options=[
                    {'label': 'Temperature', 'value': 'temperature'},
                    {'label': 'Humidity', 'value': 'humidity'},
                    {'label': 'Wind Speed', 'value': 'wind_speed'},
                    {'label': 'Precipitation Probability', 'value': 'precipitation_probability'}
                ],
                value='temperature',
                clearable=False,
                style={'width': '50%'}
            ),
            dcc.Graph(id='weather-graph')
        ])
    elif tab == 'map':
        if not data:
            return html.H3("Нет данных для отображения маршрута")

        df = pd.DataFrame(data)

        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
            lat=df['lat'],
            lon=df['lon'],
            mode='markers+lines',
            marker=go.scattermapbox.Marker(size=10, color='blue'),
            text=df.apply(lambda row: f"{row['city']} (Day {row['day']}): {row['temperature']}°C", axis=1),
            hoverinfo='text'
        ))

        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                zoom=3,
                center=dict(lat=55, lon=40)
            ),
            height=600,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        return dcc.Graph(figure=fig)


@dash_app.callback(
    Output('weather-graph', 'figure'),
    [Input('metric-selector', 'value')]
)
def update_graph(selected_metric):
    global days
    df = pd.DataFrame(data)

    if df.empty:
        return px.scatter(title="No Data Available")

    if days == 1:
        fig = px.bar(
            df,
            x="city",
            y=selected_metric,
            color="city",
            title=f"Weather Metric: {selected_metric.capitalize()} (1 Day)",
            labels={selected_metric: selected_metric.capitalize()},
        )
    else:
        fig = px.line(
            df,
            x="day",
            y=selected_metric,
            color="city",
            markers=True,
            title=f"Weather Metric: {selected_metric.capitalize()}",
            labels={'day': 'Day', selected_metric: selected_metric.capitalize()}
        )

    return fig


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@app.route('/eval', methods=['POST'])
def evaluate():
    global data, days
    try:

        points = request.json['points']
        points.append(points.pop(1))
        print(points)
        days = request.json['days']
        weather_list = []

        for item in points:
            weather_by_city = api.get_weather_by_city_name(item, days)
            weather_list.extend(weather_by_city)

        data = [
            {
                **item.to_json(),
                "lat": item.lat,
                "lon": item.lon
            }
            for item in weather_list if item.day < days
        ]

        return redirect('/dashboard/')
    except LocationNotFoundError:
        return render_template('result.html', result="Location not found")
    except Exception as ex:
        print(ex)
        return render_template('result.html', result="Unpredictable exception")


if __name__ == '__main__':
    app.run(debug=True)
