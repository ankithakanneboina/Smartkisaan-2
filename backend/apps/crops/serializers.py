from rest_framework import serializers

from .models import Crop, CropRecommendation


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = (
            "id", "name", "season", "water_requirement",
            "soil_requirement", "growing_duration_days", "farming_tips",
        )


class CropRecommendationRequestSerializer(serializers.Serializer):
    """Validates the §5 input form before it reaches the predictor."""
    soil_type = serializers.CharField(required=False, allow_blank=True)
    n = serializers.FloatField(required=False, allow_null=True)
    p = serializers.FloatField(required=False, allow_null=True)
    k = serializers.FloatField(required=False, allow_null=True)
    ph = serializers.FloatField(required=False, allow_null=True, min_value=0, max_value=14)
    temperature = serializers.FloatField(required=False, allow_null=True)
    humidity = serializers.FloatField(required=False, allow_null=True, min_value=0, max_value=100)
    rainfall = serializers.FloatField(required=False, allow_null=True, min_value=0)
    season = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    land_area = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    irrigation_available = serializers.BooleanField(required=False, default=False)


class CropRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropRecommendation
        fields = (
            "id", "soil_type", "nitrogen", "phosphorus", "potassium", "ph",
            "temperature", "humidity", "rainfall", "season", "land_area",
            "irrigation_available", "predicted_crops", "created_at",
        )
        read_only_fields = fields
