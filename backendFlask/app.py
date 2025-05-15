from flask import Flask
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    weather = requests.get("https://archive-api.open-meteo.com/v1/archive?latitude=42.0&longitude=-93.0&start_date=2020-06-01&end_date=2020-08-31&daily=precipitation_sum,temperature_2m_max&timezone=America/Chicago").json()
    weather_df = pd.DataFrame({
        'date': weather['daily']['time'],
        'precip': weather['daily']['precipitation_sum'],
        'temp_max': weather['daily']['temperature_2m_max']
    })
    avg_precip = weather_df['precip'].mean()
    avg_temp = weather_df['temp_max'].mean()

    nass = requests.get("https://quickstats.nass.usda.gov/api/api_GET/?key=FCDEFFA0-80A5-32A4-AC39-07089250C1DA&commodity_desc=CORN&year=2020&state_alpha=IA&statisticcat_desc=YIELD&format=JSON").json()
    yield_value = nass['data'][0]['Value']

    return f"""
    <h1>Dane dla stanu Iowa, rok 2020</h1>
    <p><strong>Średnie opady:</strong> {avg_precip:.2f} mm</p>
    <p><strong>Średnia temperatura:</strong> {avg_temp:.2f} °C</p>
    <p><strong>Plon kukurydzy:</strong> {yield_value} bushels/acre</p>
    """

if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')
