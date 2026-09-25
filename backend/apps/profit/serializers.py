from decimal import Decimal

from rest_framework import serializers

from .models import ProfitCalculation


class ProfitCalculationRequestSerializer(serializers.Serializer):
    """Validates the §13 input form before the view computes anything."""
    crop = serializers.CharField(required=False, allow_blank=True)
    land_area = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=Decimal('0'))
    seed_cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0, min_value=Decimal('0'))
    fertilizer_cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0, min_value=Decimal('0'))
    labour_cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0, min_value=Decimal('0'))
    irrigation_cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0, min_value=Decimal('0'))
    pesticide_cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0, min_value=Decimal('0'))
    other_expenses = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0, min_value=Decimal('0'))
    expected_yield = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0'))
    expected_selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0'))


class ProfitCalculationSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source="crop.name", read_only=True, default=None)

    class Meta:
        model = ProfitCalculation
        fields = (
            "id", "crop", "crop_name", "land_area",
            "seed_cost", "fertilizer_cost", "labour_cost", "irrigation_cost",
            "pesticide_cost", "other_expenses", "expected_yield", "expected_selling_price",
            "total_investment", "expected_revenue", "expected_profit",
            "cost_per_acre", "revenue_per_acre", "profit_margin_percent",
            "created_at",
        )
        read_only_fields = fields
