from django.conf import settings
from django.db import models

from apps.crops.models import Crop


class Fertilizer(models.Model):
    """Static fertilizer catalog — seeded with demo data in Phase 3/§34."""
    name = models.CharField(max_length=100, unique=True)
    fertilizer_type = models.CharField(max_length=50, blank=True)  # e.g. "Urea", "DAP", "Organic"
    application_method = models.TextField(blank=True)
    precautions = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FertilizerRecommendation(models.Model):
    """
    One saved fertilizer-recommendation request + result, per spec §9.
    predicted_fertilizers mirrors CropRecommendation.predicted_crops —
    loose JSON until ml_models.fertilizer_recommendation.predictor's
    output shape is finalized in Phase 3.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fertilizer_recommendations"
    )
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    soil_type = models.CharField(max_length=50, blank=True)
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    growth_stage = models.CharField(max_length=50, blank=True)
    land_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    predicted_fertilizers = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"FertilizerRecommendation for {self.user} ({self.created_at:%Y-%m-%d})"
