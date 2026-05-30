from flask import Flask, render_template
import os, requests

app = Flask(__name__)

WEATHER_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book-service:5001")
FORECAST_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL", "http://review-service:5002")

@app.route('/')
def index():
    cities = []
    try:
        cities = requests.get(f"{WEATHER_SERVICE_URL}/weather", timeout=2).json()
        for c in cities:
            c['forecast'] = requests.get(
                f"{FORECAST_SERVICE_URL}/forecast?city_id={c['id']}", timeout=2
            ).json()
    except Exception as e:
        cities = [{"id": 0, "city": f"Connection Error: {str(e)}", "country": "",
                   "temp": 0, "condition": "Error", "humidity": 0, "wind": 0, "forecast": []}]
    return render_template('index.html', cities=cities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
