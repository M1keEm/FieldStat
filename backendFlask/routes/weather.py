import os
from flask import Blueprint, request, jsonify
from backendFlask.services.apiFetchData import STATE_CAPITALS, get_weather_data
from dotenv import load_dotenv

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather')
def weather():
    state = request.args.get("state", "Iowa").title()
    year = int(request.args.get("year", 2022))
    coords = STATE_CAPITALS.get(state)
    if not coords:
        return jsonify(message=f"Coordinates for {state} not found."), 404
    try:
        avg_temp, total_prec = get_weather_data(*coords, year)
        return jsonify(state=state, year=year, avg_temp_C=avg_temp, total_precip_mm=total_prec)
    except Exception as e:
        return jsonify(message=str(e)), 500