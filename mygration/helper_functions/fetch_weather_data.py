import requests_cache
from retry_requests import retry
from datetime import datetime

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

URL = "https://api.open-meteo.com/v1/forecast"

def _first(x, default=None):
    """Return x[0] if list/tuple; if x is None use default."""
    if x is None:
        return default
    return x[0] if isinstance(x, (list, tuple)) else x


def fetch_weather_data(plan):
    lat, lon = map(float, plan.location.split(","))

    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "current": (
            "temperature_2m,apparent_temperature,relative_humidity_2m,"
            "wind_speed_10m,weather_code"
        ),
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "forecast_days": 7,
    }

    data = retry_session.get(URL, params=params, timeout=10).json()

    # "current" (arrays) OR "current_weather" (scalars)
    cur = data.get("current") or data.get("current_weather", {})

    # pull with graceful fallbacks
    temp_f        = _first(cur.get("temperature_2m") or cur.get("temperature"), 0)
    feels_like_f  = _first(cur.get("apparent_temperature"), temp_f)
    humidity      = int(_first(cur.get("relative_humidity_2m") or cur.get("relative_humidity"), 0))
    wind_mph      = _first(cur.get("wind_speed_10m") or cur.get("wind_speed"), 0)
    wcode         = _first(cur.get("weather_code"), 0)

    weather_data = {
        "temperature": round(temp_f),
        "feels_like":  round(feels_like_f),
        "temp_unit":   "°F",
        "description": f"Code {wcode}",
        "icon_url":    f"/static/weather/code_{wcode}.svg",
        "windspeed":   round(wind_mph),
        "wind_unit":   "mph",
        "humidity":    humidity,
        "daily": [],
    }

    # ------------- 3-day forecast ---------------------------------
    daily = data["daily"]
    for i in range(3):
        d_code    = daily["weather_code"][i]
        date_obj  = datetime.fromisoformat(daily["time"][i])
        weather_data["daily"].append({
            "date":     date_obj.strftime("%a"),
            "tempmax":  round(daily["temperature_2m_max"][i]),
            "tempmin":  round(daily["temperature_2m_min"][i]),
            "icon_url": f"/static/weather/code_{d_code}.svg",
            "description": f"Code {d_code}",
        })

    return weather_data