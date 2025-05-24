import os
from flask import Blueprint, request, jsonify
from backendFlask.config import Config
from backendFlask.services.apiFetchData import get_crop_yield_by_state, enrich_with_weather
from backendFlask.services.graphic import plot_total_production_by_state

plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/crop_yield')
def crop_yield():
    commodity = request.args.get("commodity", "CORN").upper()
    year = int(request.args.get("year", 2022))
    yields = get_crop_yield_by_state(Config.API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    return jsonify(data=enriched)

@plot_bp.route('/plot')
def plot():
    commodity = request.args.get("commodity", "CORN").upper()
    year = int(request.args.get("year", 2022))
    yields = get_crop_yield_by_state(Config.API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, "total_production.png")
    plot_total_production_by_state(enriched, save_path=plot_path)
    return jsonify(message="Plot created", path=f"/{plot_path}")