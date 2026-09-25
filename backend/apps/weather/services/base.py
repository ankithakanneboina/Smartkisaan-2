from abc import ABC, abstractmethod


class WeatherProvider(ABC):
    """
    Common interface every weather provider implements. The rest of the
    app (views, alert logic, dashboard serializer) only ever talks to
    this interface — swapping providers is a one-line settings change,
    never a call-site change.
    """

    @abstractmethod
    def get_current_and_forecast(self, *, location_name: str, latitude=None, longitude=None) -> dict:
        """
        Must return a dict shaped like:
        {
            "location_name": str,
            "temperature_c": float,
            "humidity_percent": float,
            "wind_kph": float,
            "rain_probability_percent": float,
            "rainfall_mm": float,
            "forecast": [ {"date": "YYYY-MM-DD", "temp_min_c": .., "temp_max_c": ..,
                            "rain_probability_percent": .., "condition": ".."}, ... ],  # 5-7 days
            "provider": str,
        }
        """
        raise NotImplementedError
