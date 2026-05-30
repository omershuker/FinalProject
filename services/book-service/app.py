import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OWM_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITIES = ["Tel Aviv", "New York", "London", "Tokyo", "Paris"]

def fetch_weather(city):
    resp = requests.get(OWM_URL, params={
        "q": city, "appid": API_KEY, "units": "metric"
    }, timeout=5)
    resp.raise_for_status()
    d = resp.json()
    return {
        "id": d["id"],
        "city": d["name"],
        "country": d["sys"]["country"],
        "temp": round(d["main"]["temp"]),
        "feels_like": round(d["main"]["feels_like"]),
        "condition": d["weather"][0]["main"],
        "description": d["weather"][0]["description"].capitalize(),
        "icon": d["weather"][0]["icon"],
        "humidity": d["main"]["humidity"],
        "wind": round(d["wind"]["speed"] * 3.6),
    }

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city:
        try:
            return jsonify(fetch_weather(city))
        except requests.HTTPError:
            return jsonify({"error": f"City '{city}' not found"}), 404
    results = []
    for c in DEFAULT_CITIES:
        try:
            results.append(fetch_weather(c))
        except Exception:
            pass
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
