import requests
import sys
# ─────────────────────────────────────────
#  CONFIG — paste your API key here
#  Get a free key at: https://openweathermap.org/api
# ─────────────────────────────────────────
API_KEY = ""
BASE_URL = ""
# ── Weather condition → emoji ──────────────────────────────────────────────────
def get_weather_emoji(condition: str) -> str:
    condition = condition.lower()
    if "thunderstorm" in condition:
        return " "
    elif "drizzle" in condition:
        return " "
    elif "rain" in condition:
        return " "
    elif "snow" in condition:
        return " "
    elif "mist" in condition or "fog" in condition or "haze" in condition:
        return " "
    elif "clear" in condition:
        return " "
    elif "cloud" in condition:
        return " "
    else:
        return " "
# ── Wind direction helper ──────────────────────────────────────────────────────
def wind_direction(degrees: int) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(degrees / 45) % 8]
# ── Fetch weather from API ─────────────────────────────────────────────────────
def fetch_weather(city: str, unit: str = "metric") -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit,
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    if response.status_code == 401:
        raise ValueError("Invalid API key. Check your key at openweathermap.org.")
    elif response.status_code == 404:
        raise ValueError(f"City '{city}' not found. Try a different spelling.")
    elif response.status_code != 200:
        raise ValueError(f"API error: {response.status_code}")
    return response.json()
# ── Pretty-print the weather ───────────────────────────────────────────────────
def display_weather(data: dict, unit: str = "metric") -> None:
    temp_unit = "°C" if unit == "metric" else "°F"
    speed_unit = "m/s" if unit == "metric" else "mph"
    city       = data["name"]
    country    = data["sys"]["country"]
    condition  = data["weather"][0]["description"].capitalize()
    emoji      = get_weather_emoji(condition)
    temp       = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min   = data["main"]["temp_min"]
    temp_max   = data["main"]["temp_max"]
    humidity   = data["main"]["humidity"]
    wind_spd   = data["wind"]["speed"]
    wind_deg   = data["wind"].get("deg", 0)
    visibility = data.get("visibility", 0) // 1000  # metres → km
    print("\n" + "═" * 44)
    print(f"  {emoji}  {city}, {country}")
    print("═" * 44)
    print(f"  Condition  : {condition}")
    print(f"  Temperature: {temp}{temp_unit}  (feels like {feels_like}{temp_unit})")
    print(f"  Range      : {temp_min}{temp_unit}  –  {temp_max}{temp_unit}")
    print(f"  Humidity   : {humidity}%")
    print(f"  Wind       : {wind_spd} {speed_unit}  {wind_direction(wind_deg)}")
    print(f"  Visibility : {visibility} km")
    print("═" * 44 + "\n")
# ── Main loop ──────────────────────────────────────────────────────────────────
def main() -> None:
    print("\n  Python Weather App")
    print("  (type 'quit' to exit)\n")
    # Choose unit system once
    unit_choice = input("Use Celsius or Fahrenheit? (C/F) [default: C]: ").strip().upper()
    unit = "imperial" if unit_choice == "F" else "metric"
    while True:
        city = input("\nEnter city name: ").strip()
        if city.lower() in ("quit", "exit", "q"):
            print("Goodbye! ")
            break
        if not city:
            print("Please enter a city name.")
            continue
        try:
            data = fetch_weather(city, unit)
            display_weather(data, unit)
        except ValueError as e:
            print(f"  
  {e}")
        except requests.exceptions.ConnectionError:
            print("  
  No internet connection.")
        except requests.exceptions.Timeout:
            print("  
  Request timed out. Try again.")
if __name__ == "__main__":
    main()
