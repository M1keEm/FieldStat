import os
from flask import current_app
from flask import Blueprint, request, jsonify, current_app
from backendFlask.config import Config
from backendFlask.services.apiFetchData import get_crop_yield_by_state, enrich_with_weather


plot_bp = Blueprint('plot', __name__)

def fetch_and_enrich_crop_yield(commodity, year):
    yields = get_crop_yield_by_state(Config.API_KEY, commodity, year)
    enriched = enrich_with_weather(yields, year)
    return enriched

@plot_bp.route('/crop_yield')
def crop_yield():
    commodity = current_app.config.get('LAST_CROP')
    year = current_app.config.get('LAST_YEAR', 2022)
    print(f"Fetching crop yield for {commodity} in {year}")

    # Get commodity from request args, fall back to stored commodity
    request_commodity = request.args.get("commodity")
    if request_commodity is None:
        if commodity is None:
            return jsonify(error="No commodity specified and no default available"), 400
        request_commodity = commodity

    request_commodity = request_commodity.upper()
    year = int(request.args.get("year", year))
    yields = get_crop_yield_by_state(Config.API_KEY, request_commodity, year)
    enriched = enrich_with_weather(yields, year)
    return jsonify(data=enriched)

