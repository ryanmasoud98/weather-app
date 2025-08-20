from colorama import Fore, Style
import datetime
from weather.weather_utils import get_coordinates, fetch_weather, WEATHER_CODES, feels_like

def display_weather(city):
    coords = get_coordinates(city)
    if not coords:
        print(Fore.RED + f"❌ Could not find city '{city}'.")
        return
    lat, lon = coords
    print(Fore.CYAN + Style.BRIGHT + f"\n📍 Coordinates for {city}: {lat}, {lon}")

    data = fetch_weather(lat, lon)
    if not data:
        print(Fore.RED + "❌ Failed to fetch weather data.")
        return

    # Current Weather
    try:
        cw = data.get("current_weather", {})
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        code = cw.get("weathercode")
        condition_text = WEATHER_CODES.get(code, "Unknown")
        fl = feels_like(temp, wind) if temp is not None and wind is not None else None

        WEATHER_EMOJIS = {
            "Clear sky": "☀️",
            "Mainly clear": "🌤️",
            "Partly cloudy": "⛅",
            "Overcast": "☁️",
            "Fog": "🌫️",
            "Slight rain": "🌦️",
            "Moderate rain": "🌧️",
            "Heavy rain": "🌧️",
            "Slight snow": "🌨️",
            "Heavy snow": "❄️",
            "Thunderstorm": "⛈️",
        }
        emoji = WEATHER_EMOJIS.get(condition_text, "")

        if temp is not None:
            if temp < 15:
                temp_color = Fore.BLUE + Style.BRIGHT
            elif temp <= 25:
                temp_color = Fore.YELLOW + Style.BRIGHT
            else:
                temp_color = Fore.RED + Style.BRIGHT
        else:
            temp_color = ""

        print(Fore.CYAN + Style.BRIGHT + "\n🌤️ Current Weather:")
        print(f"Temperature: {temp_color}{temp:.1f}°C" if temp is not None else "Temperature: N/A")
        print(Fore.MAGENTA + f"Feels Like: {fl:.1f}°C" if fl is not None else "Feels Like: N/A")
        print(Fore.YELLOW + f"Condition: {condition_text} {emoji}")
        print(Fore.BLUE + f"Wind Speed: {wind:.1f} km/h" if wind is not None else "Wind Speed: N/A")
    except Exception:
        print(Fore.RED + "❌ Current weather unavailable.")

    # Daily Forecast
    try:
        daily = data.get("daily", {})
        times = daily.get("time", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        rain = daily.get("precipitation_sum", [])

        print(Fore.GREEN + Style.BRIGHT + "\n📅 7-Day Weather Forecast:")
        for i in range(len(times)):
            max_color = Fore.RED + Style.BRIGHT if tmax[i] > 25 else (Fore.YELLOW + Style.BRIGHT if tmax[i] <= 25 else Fore.BLUE + Style.BRIGHT)
            min_color = Fore.BLUE + Style.BRIGHT if tmin[i] < 15 else (Fore.YELLOW + Style.BRIGHT if tmin[i] <= 25 else Fore.RED + Style.BRIGHT)
            rain_warn = " ⚠️" if rain[i] > 10 else ""
            print(f"{Fore.GREEN + times[i]}: Max {max_color}{tmax[i]:.1f}°C | Min {min_color}{tmin[i]:.1f}°C | Rain {Fore.CYAN}{rain[i]:.1f}mm{rain_warn}")
    except Exception:
        print(Fore.RED + "❌ Failed to fetch daily forecast.")

    # Hourly Forecast
    try:
        hourly = data.get("hourly", {})
        h_times = hourly.get("time", [])
        h_temp = hourly.get("temperature_2m", [])

        now = datetime.datetime.now()
        start_index = 0
        for i, t in enumerate(h_times):
            t_dt = datetime.datetime.fromisoformat(t)
            if t_dt >= now:
                start_index = i
                break

        print(Fore.YELLOW + Style.BRIGHT + "\n🌡️ Hourly Temperature Forecast (next 24 hours):")
        for i in range(start_index, min(start_index+24, len(h_times))):
            temp_color = Fore.BLUE + Style.BRIGHT if h_temp[i] < 15 else (Fore.YELLOW + Style.BRIGHT if h_temp[i] <= 25 else Fore.RED + Style.BRIGHT)
            print(f"{h_times[i]}: {temp_color}{h_temp[i]:.1f}°C")
    except Exception:
        print(Fore.RED + "❌ Failed to fetch hourly forecast.")

def weather_loop():
    while True:
        city = input("\nEnter city name (or type 'exit' to logout): ").strip()
        if city.lower() == "exit":
            print("Returning to main menu...\n")
            break
        display_weather(city)
