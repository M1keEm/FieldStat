from backendFlask import create_app
import os
from dotenv import load_dotenv
from flask import request, jsonify
from flask_cors import CORS
from backendFlask.services.apiFetchData import get_crop_yield_by_state, STATE_CAPITALS, get_weather_data, enrich_with_weather
from backendFlask.services.graphic import plot_total_production_by_state

# Load environment variables once
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = create_app()
CORS(app)

@app.route('/')
def index():
    return """
    <h1>Welcome to the Crop Yield API</h1>
    <p>Use the endpoint /crop_yield to get crop yield data.</p>
    """

@app.route('/crop_yield')
def crop_yield():
    commodity = request.args.get("commodity", "CORN").upper()
    year = int(request.args.get("year", 2022))
    yields = get_crop_yield_by_state(API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    return jsonify(data=enriched)

@app.route('/weather')
def weather():
    state = request.args.get("state", "Iowa").title()
    year = int(request.args.get("year", 2022))
    coords = STATE_CAPITALS.get(state)
    if not coords:
        return jsonify(error=f"Coordinates for {state} not found."), 404
    try:
        avg_temp, total_prec = get_weather_data(*coords, year)
        return jsonify(state=state, year=year, avg_temp_C=avg_temp, total_precip_mm=total_prec)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/plot')
def plot():
    commodity = request.args.get("commodity", "CORN").upper()
    year = int(request.args.get("year", 2022))
    yields = get_crop_yield_by_state(API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, "total_production.png")
    plot_total_production_by_state(enriched, save_path=plot_path)
    return jsonify(message="Plot created", path=f"/{plot_path}")

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error=str(e)), 500

@app.route('/api/crops', methods=['POST'])
def handle_crop_data():
    try:
        data = request.get_json()
        
        print(f"Requested Data: Year - {data['year']}, Crop - {data['crop']}")
        
        return jsonify({
            "message": f"Data saved for {data['crop']} ({data['year']})",
            "status": "success"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 400

if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, request
# import pandas as pd
# import matplotlib.pyplot as plt
# import io
# import base64
#
# from backendFlask import create_app
#
# app = create_app()
#
# @app.route('/', methods=['GET'])
# def index():
#     load_dotenv()
#     API_KEY = os.getenv('API_KEY')
#
#     # Pobieramy daty z parametrów GET (lub ustawiamy domyślne)
#     start_date = request.args.get('start_date', '2020-06-01')
#     end_date = request.args.get('end_date', '2020-08-31')
#     year = start_date.split('-')[0]
#     # Pobieranie danych pogodowych z podanymi datami
#     weather_url = (
#         f"https://archive-api.open-meteo.com/v1/archive?"
#         f"latitude=42.0&longitude=-93.0&start_date={start_date}&end_date={end_date}"
#         f"&daily=precipitation_sum,temperature_2m_max&timezone=America/Chicago"
#     )
#     weather = requests.get(weather_url).json()
#     temps = weather['daily']['temperature_2m_max']
#     avg_temp = sum(temps) / len(temps)
#
#     weather_df = pd.DataFrame({
#         'date': weather['daily']['time'],
#         'precip': weather['daily']['precipitation_sum'],
#         'temp_max': weather['daily']['temperature_2m_max']
#     })
#     avg_precip = weather_df['precip'].mean()
#
#     # Pobieranie danych o plonach (bez zmian)
#     nass_url = (
#         f"https://quickstats.nass.usda.gov/api/api_GET/?key={API_KEY}"
#         f"&commodity_desc=CORN&year={year}&state_alpha=IA&statisticcat_desc=YIELD&format=JSON"
#     )
#     nass = requests.get(nass_url).json()
#     yield_value = nass['data'][0]['Value']
#
#     # Tworzenie wykresu słupkowego
#     # labels = ['Śr. temperatura [°C]', 'Plon kukurydzy [bushels/acre]']
#     # values = [avg_temp, yield_value]
#     # colors = ['orange', 'green']
#
#     # plt.figure(figsize=(6, 4))
#     # plt.bar(labels, values, color=colors)
#     # plt.title('Średnia temperatura vs plon kukurydzy (Iowa, 2020)')
#     # plt.ylabel('Wartość')
#     # plt.grid(axis='y')
#
#     # img = io.BytesIO()
#     # plt.savefig(img, format='png')
#     # plt.close()
#     # img.seek(0)
#     # plot_url = base64.b64encode(img.getvalue()).decode()
#
#     # Formularz HTML + wyświetlenie wyników
#     return f"""
#     <h1>Dane dla stanu Iowa, rok 2020</h1>
#     <form method="get" action="/">
#         <label>Data początkowa: <input type="date" name="start_date" value="{start_date}"></label><br><br>
#         <label>Data końcowa: <input type="date" name="end_date" value="{end_date}"></label><br><br>
#         <button type="submit">Pokaż dane</button>
#     </form>
#     <hr>
#     <p><strong>Od: </strong> {start_date} </p>
#     <p><strong>Do: </strong> {end_date} </p>
#     <p><strong>Średnie opady:</strong> {avg_precip:.2f} mm</p>
#     <p><strong>Średnia temperatura:</strong> {avg_temp:.2f} °C</p>
#     <p><strong>Plon kukurydzy:</strong> {yield_value} bushels/acre</p>
#     <hr>
#     """
