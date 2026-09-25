from rest_framework import serializers

from .models import MarketPrice


class MarketPriceSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source="crop.name", read_only=True)

    class Meta:
        model = MarketPrice
        fields = (
            "id", "crop", "crop_name", "market_name", "current_price",
            "min_price", "max_price", "unit", "recorded_date", "updated_at",
        )
        read_only_fields = ("id", "updated_at")


class MarketTrendPointSerializer(serializers.Serializer):
    """One point in a crop's price-history trend line."""
    date = serializers.DateField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
