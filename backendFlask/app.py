from backendFlask import create_app
import os
from dotenv import load_dotenv
from flask import request, jsonify
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

if __name__ == "__main__":
    app.run(debug=True)