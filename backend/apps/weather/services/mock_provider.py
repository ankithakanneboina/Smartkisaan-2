import random
from datetime import date, timedelta

from .base import WeatherProvider


class MockWeatherProvider(WeatherProvider):
    """
    Deterministic-ish fake data so the dashboard, alerts and forecast
    UI are fully buildable and testable before a real WEATHER_API_KEY
    is configured. Never presented as a live reading anywhere in the
    API response — callers get provider="mock" back explicitly.
    """

    CONDITIONS = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Thunderstorm"]

    def get_current_and_forecast(self, *, location_name: str, latitude=None, longitude=None) -> dict:
        rng = random.Random(location_name)  # stable-ish per location within a process
        forecast = []
        for i in range(7):
            day = date.today() + timedelta(days=i)
            forecast.append(
                {
                    "date": day.isoformat(),
                    "temp_min_c": round(rng.uniform(20, 26), 1),
                    "temp_max_c": round(rng.uniform(30, 38), 1),
                    "rain_probability_percent": rng.randint(0, 80),
                    "condition": rng.choice(self.CONDITIONS),
                }
            )
        return {
            "location_name": location_name or "Unknown location",
            "temperature_c": round(rng.uniform(24, 34), 1),
            "humidity_percent": round(rng.uniform(40, 85), 1),
            "wind_kph": round(rng.uniform(2, 25), 1),
            "rain_probability_percent": rng.randint(0, 70),
            "rainfall_mm": round(rng.uniform(0, 15), 1),
            "forecast": forecast,
            "provider": "mock",
        }
