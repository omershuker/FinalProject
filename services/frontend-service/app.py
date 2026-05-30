import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

WEATHER_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book-service:5001")
FORECAST_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL", "http://review-service:5002")

@app.route('/')
def index():
    search = request.args.get('city', '').strip()
    cities = []
    error = None

    try:
        if search:
            resp = requests.get(f"{WEATHER_SERVICE_URL}/weather",
                                params={"city": search}, timeout=5)
            if resp.status_code == 404:
                error = f"City '{search}' not found."
            else:
                city = resp.json()
                forecast_resp = requests.get(f"{FORECAST_SERVICE_URL}/forecast",
                                             params={"city": city['city']}, timeout=5)
                city['forecast'] = forecast_resp.json() if forecast_resp.ok else []
                cities = [city]
        else:
            cities = requests.get(f"{WEATHER_SERVICE_URL}/weather", timeout=10).json()
            for c in cities:
                forecast_resp = requests.get(f"{FORECAST_SERVICE_URL}/forecast",
                                             params={"city": c['city']}, timeout=5)
                c['forecast'] = forecast_resp.json() if forecast_resp.ok else []
    except Exception as e:
        error = f"Service error: {str(e)}"

    return render_template('index.html', cities=cities, search=search, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
