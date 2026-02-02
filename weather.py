import requests
import json
from datetime import datetime

API_KEY = "8d9d3b595ae6c87acc67537a3d0c6506"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
HISTORY_FILE = "weather_history.json"


def save_history(record):
    try:
        with open(HISTORY_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        weather = response.json()

        if weather["cod"] != 200:
            print("❌ API Error:", weather.get("message", "Unknown error"))
            return


        record = {
            "city": city,
            "temperature": weather["main"]["temp"],
            "condition": weather["weather"][0]["description"],
            "humidity": weather["main"]["humidity"],
            "wind_speed": weather["wind"]["speed"],
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        save_history(record)

        print("\n🌦️ Weather Report")
        print("---------------------")
        print(f"📍 City: {record['city']}")
        print(f"🌡️ Temperature: {record['temperature']}°C")
        print(f"☁️ Condition: {record['condition'].capitalize()}")
        print(f"💧 Humidity: {record['humidity']}%")
        print(f"💨 Wind Speed: {record['wind_speed']} m/s")

    except requests.exceptions.RequestException:
        print("⚠️ Network error.")


# -------- MAIN PROGRAM --------
while True:
    city_name = input("\nEnter city name (or 'exit' to quit): ")
    if city_name.lower() == "exit":
        print("👋 Exiting Weather App")
        break

    get_weather(city_name)

