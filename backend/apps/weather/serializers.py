from rest_framework import serializers

from .models import WeatherRecord


class WeatherRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields = (
            "location_name",
            "temperature_c",
            "humidity_percent",
            "wind_kph",
            "rain_probability_percent",
            "rainfall_mm",
            "forecast",
            "alerts",
            "provider",
            "fetched_at",
        )
