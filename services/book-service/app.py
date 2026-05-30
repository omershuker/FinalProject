from flask import Flask, jsonify

app = Flask(__name__)

cities = [
    {"id": 1, "city": "Tel Aviv", "country": "Israel", "temp": 28, "condition": "Sunny", "humidity": 65, "wind": 12},
    {"id": 2, "city": "New York", "country": "USA", "temp": 22, "condition": "Partly Cloudy", "humidity": 70, "wind": 15},
    {"id": 3, "city": "London", "country": "UK", "temp": 15, "condition": "Rainy", "humidity": 85, "wind": 20},
    {"id": 4, "city": "Tokyo", "country": "Japan", "temp": 25, "condition": "Clear", "humidity": 60, "wind": 8},
]

@app.route('/weather', methods=['GET'])
def get_weather():
    return jsonify(cities)

@app.route('/weather/<int:city_id>', methods=['GET'])
def get_city_weather(city_id):
    city = next((c for c in cities if c['id'] == city_id), None)
    return jsonify(city) if city else (jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
