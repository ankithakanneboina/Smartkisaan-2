import requests
from django.conf import settings

from .base import WeatherProvider


class OpenWeatherMapProvider(WeatherProvider):
    """
    Real provider — only instantiated when WEATHER_API_KEY is set
    (see get_weather_provider() in service.py). Talks to OpenWeatherMap's
    One Call API; swap the two request calls below if a different
    vendor is chosen later, the interface doesn't change.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_and_forecast(self, *, location_name: str, latitude=None, longitude=None) -> dict:
        current = requests.get(
            f"{self.BASE_URL}/weather",
            params={"q": location_name, "lat": latitude, "lon": longitude,
                    "appid": self.api_key, "units": "metric"},
            timeout=5,
        ).json()

        forecast_raw = requests.get(
            f"{self.BASE_URL}/forecast",
            params={"q": location_name, "lat": latitude, "lon": longitude,
                    "appid": self.api_key, "units": "metric"},
            timeout=5,
        ).json()

        forecast = self._condense_forecast(forecast_raw.get("list", []))

        return {
            "location_name": current.get("name") or location_name,
            "temperature_c": current.get("main", {}).get("temp"),
            "humidity_percent": current.get("main", {}).get("humidity"),
            "wind_kph": (current.get("wind", {}).get("speed") or 0) * 3.6,
            "rain_probability_percent": None,  # not in the free /weather endpoint
            "rainfall_mm": (current.get("rain", {}) or {}).get("1h", 0),
            "forecast": forecast,
            "provider": "openweathermap",
        }

    @staticmethod
    def _condense_forecast(entries):
        """Collapse OWM's 3-hourly list into one summary per day, 5-7 days."""
        by_day = {}
        for entry in entries:
            day = entry["dt_txt"].split(" ")[0]
            by_day.setdefault(day, []).append(entry)

        result = []
        for day, day_entries in list(by_day.items())[:7]:
            temps = [e["main"]["temp"] for e in day_entries]
            pops = [e.get("pop", 0) * 100 for e in day_entries]
            result.append(
                {
                    "date": day,
                    "temp_min_c": min(temps),
                    "temp_max_c": max(temps),
                    "rain_probability_percent": max(pops) if pops else 0,
                    "condition": day_entries[len(day_entries) // 2]["weather"][0]["main"],
                }
            )
        return result
