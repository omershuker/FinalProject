from flask import Flask, jsonify, request

app = Flask(__name__)

forecasts = [
    {"city_id": 1, "day": "Tomorrow", "temp": 30, "condition": "Sunny"},
    {"city_id": 1, "day": "In 2 days", "temp": 27, "condition": "Partly Cloudy"},
    {"city_id": 2, "day": "Tomorrow", "temp": 20, "condition": "Sunny"},
    {"city_id": 2, "day": "In 2 days", "temp": 18, "condition": "Rainy"},
    {"city_id": 3, "day": "Tomorrow", "temp": 16, "condition": "Cloudy"},
    {"city_id": 3, "day": "In 2 days", "temp": 14, "condition": "Rainy"},
    {"city_id": 4, "day": "Tomorrow", "temp": 26, "condition": "Clear"},
    {"city_id": 4, "day": "In 2 days", "temp": 23, "condition": "Cloudy"},
]

@app.route('/forecast', methods=['GET'])
def get_forecast():
    city_id = request.args.get('city_id', type=int)
    if city_id:
        return jsonify([f for f in forecasts if f['city_id'] == city_id])
    return jsonify(forecasts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
