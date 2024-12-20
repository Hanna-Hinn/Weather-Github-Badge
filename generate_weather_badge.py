import requests
import json
import sys
import os

def get_weather_json(city, rapidapi_key, language="EN"):
    url = f"https://open-weather13.p.rapidapi.com/city/{city}/{language}"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "open-weather13.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather data. Status code: {response.status_code}, Response: {response.text}")

    data = response.json()

    temp_f = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    city_name = data["name"]

    celsius = (temp_f - 32) * 5.0/9.0

    if celsius < 10:
        color = "blue"
    elif celsius < 20:
        color = "green"
    elif celsius < 30:
        color = "yellow"
    else:
        color = "red"

    # Construct the shields.json data structure for the badge
    shields_json = {
        "schemaVersion": 1,
        "label": f"{city_name} Weather",
        "message": f"{celsius:.1f}°C {desc}",
        "color": color
    }

    return shields_json

if __name__ == "__main__":
    # Prefer city from environment variable if set, otherwise from CLI arg
    city = os.environ.get("CITY")
    if not city and len(sys.argv) > 1:
        city = sys.argv[1]
    if not city:
        print("Error: City name not provided. Set the CITY environment variable or pass it as a command-line argument.")
        sys.exit(1)

    rapidapi_key = os.environ.get("RAPIDAPI_KEY")
    if not rapidapi_key:
        print("Error: RAPIDAPI_KEY environment variable not set.")
        sys.exit(1)

    shields_json = get_weather_json(city, rapidapi_key)
    # Write the output to weather.json
    with open("weather.json", "w") as f:
        json.dump(shields_json, f, indent=2)
