from rest_framework import serializers

from .models import Fertilizer, FertilizerRecommendation


class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = ("id", "name", "fertilizer_type", "application_method", "precautions")


class FertilizerRecommendationRequestSerializer(serializers.Serializer):
    """Validates the §9 input form before it reaches the predictor."""
    crop = serializers.CharField(required=False, allow_blank=True)
    soil_type = serializers.CharField(required=False, allow_blank=True)
    n = serializers.FloatField(required=False, allow_null=True)
    p = serializers.FloatField(required=False, allow_null=True)
    k = serializers.FloatField(required=False, allow_null=True)
    ph = serializers.FloatField(required=False, allow_null=True, min_value=0, max_value=14)
    growth_stage = serializers.CharField(required=False, allow_blank=True)
    land_area = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)


class FertilizerRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerRecommendation
        fields = (
            "id", "crop", "soil_type", "nitrogen", "phosphorus", "potassium",
            "ph", "growth_stage", "land_area", "predicted_fertilizers", "created_at",
        )
        read_only_fields = fields
