from django.db import models


class WeatherRecord(models.Model):
    """
    Cached snapshot of a weather lookup for a location, so repeated
    dashboard loads don't re-hit the external API every time. Section
    11's forecast/alerts endpoints read through this cache.
    """
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    temperature_c = models.FloatField(null=True, blank=True)
    humidity_percent = models.FloatField(null=True, blank=True)
    wind_kph = models.FloatField(null=True, blank=True)
    rain_probability_percent = models.FloatField(null=True, blank=True)
    rainfall_mm = models.FloatField(null=True, blank=True)

    forecast = models.JSONField(default=list, blank=True)  # list of daily forecast dicts
    alerts = models.JSONField(default=list, blank=True)     # e.g. ["heavy_rain", "heat_wave"]
    provider = models.CharField(max_length=30, default="mock")  # which provider produced this

    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fetched_at"]

    def __str__(self):
        return f"{self.location_name} @ {self.fetched_at:%Y-%m-%d %H:%M}"
