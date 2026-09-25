from django.contrib import admin

from .models import ProfitCalculation


@admin.register(ProfitCalculation)
class ProfitCalculationAdmin(admin.ModelAdmin):
    list_display = ("user", "crop", "land_area", "expected_profit", "profit_margin_percent", "created_at")
    list_filter = ("crop",)
