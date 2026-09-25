from django.contrib import admin

from .models import WeatherRecord


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ("location_name", "temperature_c", "provider", "fetched_at")
    list_filter = ("provider",)
    search_fields = ("location_name",)
