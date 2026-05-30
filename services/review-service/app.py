import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

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

@app.route('/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "city parameter required"}), 400

    resp = requests.get(
        f"https://wttr.in/{city}?format=j1",
        headers={"User-Agent": "weather-app/1.0"},
        timeout=5
    )
    if resp.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    forecast = []
    for day in resp.json().get("weather", [])[:5]:
        hourly = day.get("hourly", [])
        noon = hourly[min(4, len(hourly) - 1)] if hourly else {}
        desc = noon.get("weatherDesc", [{}])[0].get("value", "Unknown")
        forecast.append({
            "date": day["date"],
            "temp_max": int(day["maxtempC"]),
            "temp_min": int(day["mintempC"]),
            "condition": desc,
            "emoji": condition_emoji(desc),
        })

    return jsonify(forecast)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
