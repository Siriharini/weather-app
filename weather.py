from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "74c316f0cdf461cd23fdc22181c82ca8")
BASE_URL = "https://openweathermap.org/api"

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data.get("cod") == "404":
            return jsonify({"error": "City not found"}), 404

        weather_info = {
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "description": weather_data["weather"][0]["description"],
            "icon": weather_data["weather"][0]["icon"],
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data["wind"]["speed"]
        }
        return jsonify(weather_info)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return jsonify({"error": f"HTTP error: {http_err.response.status_code} - {http_err.response.text}"}), http_err.response.status_code
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return jsonify({"error": "Network connection error. Please check your internet."}), 500
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return jsonify({"error": "Request timed out. Please try again."}), 500
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return jsonify({"error": "An unexpected error occurred while fetching weather data."}), 500
    except KeyError as key_err:
        print(f"Key error in weather data: {key_err}")
        return jsonify({"error": "Unexpected data format from weather API."}), 500
    except Exception as e:
        print(f"An unhandled error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)