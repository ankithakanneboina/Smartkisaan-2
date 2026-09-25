from django.contrib import admin

from .models import MarketPrice


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ("crop", "market_name", "current_price", "unit", "recorded_date")
    list_filter = ("market_name",)
    search_fields = ("crop__name", "market_name")
