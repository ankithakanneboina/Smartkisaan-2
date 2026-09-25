from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from ..models import WeatherRecord
from .mock_provider import MockWeatherProvider

CACHE_MINUTES = 30


def get_weather_provider():
    """
    Single switch point: real provider if WEATHER_API_KEY is set,
    otherwise the mock. Nothing else in the codebase should import a
    provider class directly.
    """
    api_key = getattr(settings, "WEATHER_API_KEY", "")
    if api_key:
        from .openweathermap_provider import OpenWeatherMapProvider
        return OpenWeatherMapProvider(api_key)
    return MockWeatherProvider()


def derive_alerts(data: dict) -> list:
    """Section 11: agriculture-specific alerts from raw provider data."""
    alerts = []
    if (data.get("rainfall_mm") or 0) > 50:
        alerts.append("heavy_rain")
    if (data.get("temperature_c") or 0) >= 40:
        alerts.append("heat_wave")
    if (data.get("wind_kph") or 0) >= 40:
        alerts.append("strong_wind")
    if (data.get("rain_probability_percent") or 0) < 10 and (data.get("rainfall_mm") or 0) == 0:
        alerts.append("low_rainfall")
    return alerts


def get_weather_for_location(location_name: str, latitude=None, longitude=None) -> WeatherRecord:
    """
    Returns a fresh-enough WeatherRecord for this location, hitting the
    provider only if the cache is older than CACHE_MINUTES or missing.
    """
    cutoff = timezone.now() - timedelta(minutes=CACHE_MINUTES)
    cached = (
        WeatherRecord.objects.filter(location_name=location_name, fetched_at__gte=cutoff)
        .order_by("-fetched_at")
        .first()
    )
    if cached:
        return cached

    provider = get_weather_provider()
    data = provider.get_current_and_forecast(
        location_name=location_name, latitude=latitude, longitude=longitude
    )
    return WeatherRecord.objects.create(
        location_name=data["location_name"],
        latitude=latitude,
        longitude=longitude,
        temperature_c=data.get("temperature_c"),
        humidity_percent=data.get("humidity_percent"),
        wind_kph=data.get("wind_kph"),
        rain_probability_percent=data.get("rain_probability_percent"),
        rainfall_mm=data.get("rainfall_mm"),
        forecast=data.get("forecast", []),
        alerts=derive_alerts(data),
        provider=data.get("provider", "mock"),
    )
