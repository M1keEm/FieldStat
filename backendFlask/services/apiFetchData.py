import os
import requests
from dotenv import load_dotenv
from backendFlask.config import Config


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


def get_weather_data(lat, lon, year):
    """Fetch average temperature and total precipitation from Open-Meteo API."""
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
    response.raise_for_status()
    data = response.json().get("daily", {})
    temps = data.get("temperature_2m_mean", [])
    precs = data.get("precipitation_sum", [])
    avg_temp = sum(temps) / len(temps) if temps else None
    total_prec = sum(precs) if precs else None
    return avg_temp, total_prec


def get_crop_yield_by_state(api_key, commodity, year):
    """Fetch yield and area planted data from USDA QuickStats API for each state and year."""
    url = "https://quickstats.nass.usda.gov/api/api_GET/"
    try:
        # Dodaj timeout do żądań USDA
        response = requests.get(url, params={
            'key': Config.API_KEY,
            'commodity_desc': commodity,
            'year': str(year),
            'statisticcat_desc': 'YIELD',
        })

        params_yield = {
            "key": api_key,
            "commodity_desc": commodity.upper(),
            "year": str(year),
            "agg_level_desc": "STATE",
            "statisticcat_desc": "YIELD",
            "prodn_practice_desc": "ALL PRODUCTION PRACTICES",
            "format": "JSON"
        }
        params_area = {
            "key": api_key,
            "commodity_desc": commodity.upper(),
            "year": str(year),
            "agg_level_desc": "STATE",
            "statisticcat_desc": "AREA PLANTED",
            "prodn_practice_desc": "ALL PRODUCTION PRACTICES",
            "format": "JSON"
        }
        yield_data = requests.get(url, params=params_yield).json().get("data", [])
        area_data = requests.get(url, params=params_area).json().get("data", [])

        # Safely parse area values, handling special values like (D) for disclosure limitations
        area_by_state = {}
        for item in area_data:
            state = item.get("state_name")
            value = item.get("Value")
            try:
                if value and not any(special in value for special in ["(D)", "(NA)", "NA", "--"]):
                    # Remove commas and convert to float
                    area_by_state[state] = float(value.replace(",", "").strip())
                else:
                    # Use None for special values indicating no data
                    area_by_state[state] = None
            except ValueError:
                # If conversion fails for any reason, use None
                print(f"Warning: Could not convert area value '{value}' for {state}")
                area_by_state[state] = None

        results = []
        seen_states = set()
        for item in yield_data:
            state = item.get("state_name")
            if state in seen_states:
                continue
            value = item.get("Value")
            unit = item.get("unit_desc")

            # Safely parse yield values, handling special values
            try:
                if value and not any(special in value for special in ["(D)", "(NA)", "NA", "--"]):
                    yield_value = float(value.replace(",", "").strip())
                else:
                    yield_value = None
            except ValueError:
                print(f"Warning: Could not convert yield value '{value}' for {state}")
                yield_value = None

            area_planted = area_by_state.get(state)
            total_production = yield_value * area_planted if yield_value is not None and area_planted is not None else None

            if unit == "BU / ACRE":
                unit = "TONS / ACRE"
                yield_value = yield_value * 0.0254 if yield_value is not None else None

            if unit == "CWT / ACRE":
                unit = "TONS / ACRE"
                yield_value = yield_value * 0.04546 if yield_value is not None else None

            results.append({
                "commodity": commodity,
                "state": state,
                "avg_temp_C": None,
                "total_precip_mm": None,
                "area_planted_acres": area_planted,
                "unit": unit,
                "total_production": total_production,
                "average_yield": yield_value
            })
            seen_states.add(state)
        return results
    except requests.exceptions.Timeout:
        print("USDA API timeout")
        return []


def enrich_with_weather(yield_data, year):
    """Enrich yield data with weather information for each state."""
    enriched = []
    for entry in yield_data:
        state = entry["state"]
        coords = STATE_CAPITALS.get(state.title())
        if not coords:
            print(f"No coordinates for {state}, skipping.")
            continue
        try:
            avg_temp, total_prec = get_weather_data(*coords, year)
        except Exception as e:
            print(f"Weather data error for {state}: {e}")
            avg_temp, total_prec = None, None
        entry["avg_temp_C"] = avg_temp
        entry["total_precip_mm"] = total_prec
        enriched.append(entry)
    return enriched
