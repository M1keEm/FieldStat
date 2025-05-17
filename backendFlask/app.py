from backendFlask import create_app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, request
# import requests
# import pandas as pd
# import matplotlib.pyplot as plt
# from dotenv import load_dotenv
# import io
# import base64
# import os
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
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
