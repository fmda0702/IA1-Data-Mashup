from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GEODB_API_KEY = os.getenv("GEODB_API_KEY")  
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  

GEODB_BASE_URL = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_term = request.form.get("city")

        headers = {
            "X-RapidAPI-Key": GEODB_API_KEY,
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
        }

        params = {"namePrefix": search_term, "limit": 10} 
        geo_response = requests.get(GEODB_BASE_URL, headers=headers, params=params)

        if geo_response.status_code == 429:
            return render_template("index.html", error="GeoDB rate limit reached. Please wait and try again.")

        if geo_response.status_code != 200:
            return render_template("index.html", error="Error fetching city data from GeoDB.")

        cities = geo_response.json().get("data", [])

        if not cities:
            return render_template("index.html", error="No cities found. Try another search term.")

        return render_template("results.html", cities=cities)

    return render_template("index.html")


@app.route("/weather/<city_id>")
def weather(city_id):
    headers = {
        "X-RapidAPI-Key": GEODB_API_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    city_response = requests.get(f"{GEODB_BASE_URL}/{city_id}", headers=headers)
    if city_response.status_code != 200:
        return render_template("index.html", error="Error fetching city details.")

    city_data = city_response.json().get("data", {})

    weather_params = {
        "lat": city_data.get("latitude"),
        "lon": city_data.get("longitude"),
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  
    }

    weather_response = requests.get(WEATHER_BASE_URL, params=weather_params)
    if weather_response.status_code != 200:
        return render_template("index.html", error="Error fetching weather data.")

    weather_data = weather_response.json()

    feels_like_diff = abs(weather_data["main"]["feels_like"] - weather_data["main"]["temp"])
    feels_like_diff = round(feels_like_diff, 2)

    combined_data = {
        "city": city_data.get("city"),
        "country": city_data.get("country"),
        "latitude": city_data.get("latitude"),
        "longitude": city_data.get("longitude"),
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "feels_like_diff": feels_like_diff,
        "description": weather_data["weather"][0]["description"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"]
    }

    return render_template("results.html", weather=combined_data)


if __name__ == "__main__":
    app.run(debug=True)
