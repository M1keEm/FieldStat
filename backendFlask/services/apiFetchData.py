import os
import requests
from dotenv import load_dotenv
from flask import request

load_dotenv()
API_KEY = os.getenv('API_KEY')

# start_date = request.args.get('start_date', '2020-06-01')
# end_date = request.args.get('end_date', '2020-08-31')

STATE_CAPITALS = {
    "Alabama": (32.3777, -86.3000),  # Montgomery
    "Alaska": (58.3019, -134.4197),  # Juneau
    "Arizona": (33.4484, -112.0740),  # Phoenix
    "Arkansas": (34.7465, -92.2896),  # Little Rock
    "California": (38.5767, -121.4944),  # Sacramento
    "Colorado": (39.7392, -104.9903),  # Denver
    "Connecticut": (41.7640, -72.6822),  # Hartford
    "Delaware": (39.1573, -75.5197),  # Dover
    "Florida": (30.4383, -84.2807),  # Tallahassee
    "Georgia": (33.7490, -84.3880),  # Atlanta
    "Hawaii": (21.3070, -157.8583),  # Honolulu
    "Idaho": (43.6150, -116.2023),  # Boise
    "Illinois": (39.7983, -89.6544),  # Springfield
    "Indiana": (39.7684, -86.1581),  # Indianapolis
    "Iowa": (41.5868, -93.6250),  # Des Moines
    "Kansas": (39.0489, -95.6771),  # Topeka
    "Kentucky": (38.2009, -84.8733),  # Frankfort
    "Louisiana": (30.4515, -91.1871),  # Baton Rouge
    "Maine": (44.3072, -69.7817),  # Augusta
    "Maryland": (38.9784, -76.4922),  # Annapolis
    "Massachusetts": (42.3601, -71.0589),  # Boston
    "Michigan": (42.7336, -84.5553),  # Lansing
    "Minnesota": (44.9537, -93.0900),  # Saint Paul
    "Mississippi": (32.2988, -90.1848),  # Jackson
    "Missouri": (38.5791, -92.1729),  # Jefferson City
    "Montana": (46.5891, -112.0391),  # Helena
    "Nebraska": (40.8136, -96.7026),  # Lincoln
    "Nevada": (39.1638, -119.7674),  # Carson City
    "New Hampshire": (43.2067, -71.5376),  # Concord
    "New Jersey": (40.2206, -74.7699),  # Trenton
    "New Mexico": (35.6870, -105.9378),  # Santa Fe
    "New York": (42.6526, -73.7562),  # Albany
    "North Carolina": (35.7796, -78.6382),  # Raleigh
    "North Dakota": (46.8083, -100.7837),  # Bismarck
    "Ohio": (39.9612, -82.9988),  # Columbus
    "Oklahoma": (35.4676, -97.5164),  # Oklahoma City
    "Oregon": (44.9429, -123.0351),  # Salem
    "Pennsylvania": (40.2732, -76.8867),  # Harrisburg
    "Rhode Island": (41.8236, -71.4222),  # Providence
    "South Carolina": (34.0007, -81.0348),  # Columbia
    "South Dakota": (44.3670, -100.3464),  # Pierre
    "Tennessee": (36.1627, -86.7816),  # Nashville
    "Texas": (30.2747, -97.7404),  # Austin
    "Utah": (40.7608, -111.8910),  # Salt Lake City
    "Vermont": (44.2601, -72.5754),  # Montpelier
    "Virginia": (37.5407, -77.4360),  # Richmond
    "Washington": (47.0379, -122.9007),  # Olympia
    "West Virginia": (38.3498, -81.6326),  # Charleston
    "Wisconsin": (43.0747, -89.3842),  # Madison
    "Wyoming": (41.1400, -104.8202),  # Cheyenne
    "District of Columbia": (38.9072, -77.0369),  # Washington D.C.
    "Puerto Rico": (18.4655, -66.1057)  # San Juan
}


def convert_bu_to_tons(data):
    """
    Konwertuje jednostki plonów z BU/ACRE na TONS/ACRE
    """
    for entry in data:
        if entry["unit"] == "BU / ACRE":
            entry["yield"] = entry["yield"] * 0.0254 if entry["yield"] is not None else None
            entry["unit"] = "TONS / ACRE"
    return data

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
