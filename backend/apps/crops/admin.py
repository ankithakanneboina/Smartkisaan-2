from django.contrib import admin

from .models import Crop, CropRecommendation


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "season", "water_requirement", "growing_duration_days")
    search_fields = ("name",)


@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "soil_type", "season", "created_at")
    list_filter = ("soil_type", "season")
