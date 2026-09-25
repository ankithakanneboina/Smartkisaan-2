from django.contrib import admin

from .models import Fertilizer, FertilizerRecommendation


@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ("name", "fertilizer_type")
    search_fields = ("name",)


@admin.register(FertilizerRecommendation)
class FertilizerRecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "crop", "soil_type", "created_at")
    list_filter = ("soil_type",)
