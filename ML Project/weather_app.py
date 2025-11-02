import requests
import os

API_KEY = "YOUR_API_KEY"  # 🔑 Get a free key from https://openweathermap.org/api
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name):
    """Fetch weather data for a given city."""
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        print("\n🌤️ Weather Report")
        print("---------------------")
        print(f"City: {city_name}")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {weather}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s\n")

    elif response.status_code == 404:
        print("❌ City not found. Please check the name and try again.")
    else:
        print("⚠️ Failed to fetch data. Please try again later.")


def main():
    print("====== Weather CLI App ======")
    while True:
        city = input("\nEnter city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("\nGoodbye! 👋")
            break
        elif city:
            get_weather(city)
        else:
            print("Please enter a valid city name.")


if __name__ == "__main__":
    main()
