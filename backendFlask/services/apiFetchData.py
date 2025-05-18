import os
import requests
from dotenv import load_dotenv
from flask import request

load_dotenv()
API_KEY = os.getenv('API_KEY')

# start_date = request.args.get('start_date', '2020-06-01')
# end_date = request.args.get('end_date', '2020-08-31')

STATE_CAPITALS = {
    "California": (34.0522, -118.2437),  # Los Angeles
    "Texas": (29.7604, -95.3698),  # Houston
    "Florida": (25.7617, -80.1918),  # Miami
    "New York": (40.7128, -74.0060),  # NYC
    "Illinois": (41.8781, -87.6298),  # Chicago
    "Pennsylvania": (40.7128, -74.0060),  # Philadelphia
    "Ohio": (39.9612, -82.9988),  # Columbus
    "Georgia": (33.7490, -84.3880),  # Atlanta
    "North Carolina": (35.2271, -80.8431),  # Charlotte
    "Michigan": (42.3314, -83.0458),  # Detroit
    "New Jersey": (40.0583, -74.4057),  # Trenton
    "Virginia": (37.5407, -77.4360),  # Richmond
    "Washington": (47.6062, -122.3321),  # Seattle
    "Arizona": (33.4484, -112.0740),  # Phoenix
    "Massachusetts": (42.3601, -71.0589),  # Boston
    "Tennessee": (36.1627, -86.7816),  # Nashville
    "Indiana": (39.7684, -86.1581),  # Indianapolis
    "Missouri": (38.6270, -90.1994),  # St. Louis
    "Maryland": (39.2904, -76.6122),  # Baltimore
    "Wisconsin": (43.0731, -89.4012),  # Madison
    "Colorado": (39.7392, -104.9903),  # Denver
    "South Carolina": (34.0003, -81.0345),  # Columbia
    "Alabama": (32.3777, -86.3009),  # Montgomery
    "Kentucky": (37.8399, -84.2700),  # Frankfort
    "Oregon": (44.0682, -121.3153),  # Salem
    "Oklahoma": (35.4676, -97.5164),  # Oklahoma City
    "Connecticut": (41.6032, -73.0877),  # Hartford
    "Iowa": (41.5868, -93.6250),  # Des Moines
    "Mississippi": (32.2988, -90.1848),  # Jackson
    "Arkansas": (34.7465, -92.2896),  # Little Rock
    "Kansas": (39.0997, -94.5786),  # Topeka
    "Utah": (40.7608, -111.8910),  # Salt Lake City
    "Nevada": (39.5296, -119.8138),  # Carson City
    "New Mexico": (35.6869, -105.9378),  # Santa Fe
    "Nebraska": (40.8136, -96.7026),  # Lincoln
    "West Virginia": (38.5976, -80.4549),  # Charleston
    "Idaho": (43.6150, -116.2023),  # Boise
    "Hawaii": (21.3069, -157.8583),  # Honolulu
    "Maine": (44.3072, -69.7817),  # Augusta
    "New Hampshire": (43.1939, -71.5724),  # Concord
    "Rhode Island": (41.5801, -71.4774),  # Providence
    "Montana": (46.5891, -112.0391),  # Helena
    "Delaware": (39.1573, -75.5244),  # Dover
    "South Dakota": (44.2998, -99.4388),  # Pierre
    "North Dakota": (46.8257, -100.7837),  # Bismarck
    "Alaska": (58.3019, -134.4197),  # Juneau
    "Vermont": (44.2601, -72.5754),  # Montpelier
    "Wyoming": (41.1400, -104.8202),  # Cheyenne
    "District of Columbia": (38.9072, -77.0369),  # Washington D.C.
    "Puerto Rico": (18.2208, -66.5901)  # San Juan
}


def get_weather_data(lat, lon, year):
    """
    Pobiera dane pogodowe (średnia temperatura i suma opadów) z Open-Meteo API
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "daily": ["temperature_2m_mean", "precipitation_sum"],
        "timezone": "America/New_York"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Błąd pogodowy: {response.status_code}")

    data = response.json().get("daily", {})
    temps = data.get("temperature_2m_mean", [])
    precs = data.get("precipitation_sum", [])

    avg_temp = sum(temps) / len(temps) if temps else None
    total_prec = sum(precs) if precs else None

    return avg_temp, total_prec


def get_crop_yield_by_state(api_key, commodity, year):
    """
    Pobiera dane o plonach dla określonego produktu w danym roku dla każdego stanu USA.

    :param api_key: Twój klucz API USDA NASS
    :param commodity: Nazwa produktu (np. 'CORN')
    :param year: Rok (np. 2022)
    :param prodn_practice: Praktyka produkcji (aktualnie 'ALL PRODUCTION PRACTICES')
    :return: Lista słowników zawierających dane o plonach
    """
    url = "https://quickstats.nass.usda.gov/api/api_GET/"
    params = {
        "key": api_key,
        "commodity_desc": commodity.upper(),
        "year": str(year),
        "agg_level_desc": "STATE",
        "statisticcat_desc": "YIELD",
        "prodn_practice_desc": "ALL PRODUCTION PRACTICES",
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Błąd podczas pobierania danych: {response.status_code}")

    data = response.json().get("data", [])
    seen_states = set()
    results = []
    counter = 0
    for item in data:
        state = item.get("state_name")
        if state in seen_states:
            continue  # Pominięcie duplikatów
        value = item.get("Value")
        unit = item.get("unit_desc")
        try:
            yield_value = float(value.replace(",", ""))
        except (ValueError, AttributeError):
            yield_value = None  # Wartość nieznana lub brak danych

        results.append({
            "state": state,
            "yield": yield_value,
            "unit": unit
        })
        seen_states.add(state)
        counter += 1

    results.append({
        "state": "State number",
        "yield": None,
        "unit": counter
    })

    return results


def enrich_with_weather(yield_data, year):
    """
    Dodaje dane pogodowe do wyników USDA.
    """
    enriched = []

    for entry in yield_data:
        state = entry["state"]
        state_title = state.title()
        coords = STATE_CAPITALS.get(state_title)

        if not coords:
            print(f"Brak współrzędnych dla {state}, pomijam.")
            continue

        lat, lon = coords
        try:
            avg_temp, total_prec = get_weather_data(lat, lon, year)
        except Exception as e:
            print(f"Błąd danych pogodowych dla {state}: {e}")
            avg_temp, total_prec = None, None

        entry.update({
            "avg_temp_C": avg_temp,
            "total_precip_mm": total_prec
        })
        enriched.append(entry)

    return enriched
