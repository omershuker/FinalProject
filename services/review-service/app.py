import os
import requests
from flask import Flask, jsonify, request
from collections import defaultdict

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OWM_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.route('/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "city parameter required"}), 400

    resp = requests.get(OWM_URL, params={
        "q": city, "appid": API_KEY, "units": "metric", "cnt": 40
    }, timeout=5)

    if resp.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    daily = defaultdict(list)
    for item in resp.json()["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily[date].append(item)

    forecast = []
    for date, items in list(daily.items())[:5]:
        noon = min(items, key=lambda x: abs(int(x["dt_txt"].split(" ")[1][:2]) - 12))
        forecast.append({
            "date": date,
            "temp": round(noon["main"]["temp"]),
            "condition": noon["weather"][0]["main"],
            "description": noon["weather"][0]["description"].capitalize(),
            "icon": noon["weather"][0]["icon"],
            "humidity": noon["main"]["humidity"],
            "wind": round(noon["wind"]["speed"] * 3.6),
        })

    return jsonify(forecast)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
