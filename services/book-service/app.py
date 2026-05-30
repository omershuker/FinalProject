import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

DEFAULT_CITIES = ["Tel Aviv", "New York", "London", "Tokyo", "Paris"]

def condition_emoji(desc):
    d = desc.lower()
    if any(w in d for w in ["sunny", "clear"]): return "☀️"
    if any(w in d for w in ["partly", "partial"]): return "⛅"
    if any(w in d for w in ["overcast", "cloudy", "cloud"]): return "☁️"
    if any(w in d for w in ["thunder", "storm"]): return "⛈️"
    if any(w in d for w in ["snow", "sleet", "blizzard"]): return "❄️"
    if any(w in d for w in ["rain", "drizzle", "shower"]): return "🌧️"
    if any(w in d for w in ["mist", "fog", "haze"]): return "🌫️"
    return "🌤️"

def fetch_weather(city):
    resp = requests.get(
        f"https://wttr.in/{city}?format=j1",
        headers={"User-Agent": "weather-app/1.0"},
        timeout=5
    )
    resp.raise_for_status()
    d = resp.json()
    current = d["current_condition"][0]
    nearest = d.get("nearest_area", [{}])[0]
    city_name = nearest.get("areaName", [{}])[0].get("value", city)
    country = nearest.get("country", [{}])[0].get("value", "")
    desc = current["weatherDesc"][0]["value"]
    return {
        "city": city_name,
        "country": country,
        "temp": int(current["temp_C"]),
        "feels_like": int(current["FeelsLikeC"]),
        "condition": desc,
        "emoji": condition_emoji(desc),
        "humidity": int(current["humidity"]),
        "wind": int(current["windspeedKmph"]),
    }

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city:
        try:
            return jsonify(fetch_weather(city))
        except Exception:
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
