import os
from flask import current_app
from flask import Blueprint, request, jsonify, current_app
from backendFlask.config import Config
from backendFlask.services.apiFetchData import get_crop_yield_by_state, enrich_with_weather
from backendFlask.services.graphic import plot_total_production_by_state


plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/crop_yield')
def crop_yield():
    crop = current_app.config.get('LAST_CROP')
    year = current_app.config.get('LAST_YEAR', 2022)
    print(f"Fetching crop yield for {crop} in {year}")
    
    commodity = request.args.get("commodity", crop).upper()
    year = int(request.args.get("year", year))
    yields = get_crop_yield_by_state(Config.API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    return jsonify(data=enriched)

@plot_bp.route('/plot')
def plot():
    crop = current_app.config.get('LAST_CROP')
    year = current_app.config.get('LAST_YEAR', 2022)

    commodity = request.args.get("commodity", crop).upper()
    year = int(request.args.get("year", year))
    yields = get_crop_yield_by_state(Config.API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, "total_production.png")
    plot_total_production_by_state(enriched, save_path=plot_path)
    return jsonify(message="Plot created", path=f"/{plot_path}")