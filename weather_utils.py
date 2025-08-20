from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import requests

# ---------------- WEATHER CODE MAPPING ----------------
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

# ---------------- GET COORDINATES ----------------
def get_coordinates(city, country="Pakistan"):
    geolocator = Nominatim(user_agent="weather_app_victus")
    try:
        location = geolocator.geocode(f"{city}, {country}", timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError):
        return None
    return None

# ---------------- FETCH WEATHER ----------------
def fetch_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m",
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

# ---------------- CALCULATE FEELS LIKE ----------------
def feels_like(temp_c, wind_kmh):
    wind_ms = wind_kmh / 3.6
    if temp_c >= 27:  # Hot weather
        return temp_c + 0.33 * wind_ms - 0.7
    elif temp_c <= 10:  # Cold weather
        return 13.12 + 0.6215*temp_c - 11.37*wind_ms**0.16 + 0.3965*temp_c*wind_ms**0.16
    else:  # Moderate temperature
        return temp_c
