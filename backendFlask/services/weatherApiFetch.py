import os
import requests
from dotenv import load_dotenv
from flask import request

load_dotenv()
API_KEY = os.getenv('API_KEY')

# start_date = request.args.get('start_date', '2020-06-01')
# end_date = request.args.get('end_date', '2020-08-31')


def fetch_weather(start_date, end_date):
    # Pobieramy daty z parametrów GET (lub ustawiamy domyślne)
    #  Pobieranie danych pogodowych z podanymi datami
    weather_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude=42.0&longitude=-93.0&start_date={start_date}&end_date={end_date}"
        f"&daily=precipitation_sum,temperature_2m_max&timezone=America/Chicago"
    )
    weather = requests.get(weather_url).json()
    temps = weather['daily']['temperature_2m_max']
    avg_temp = sum(temps) / len(temps)


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
            continue # Pominięcie duplikatów
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
