from django.conf import settings
from django.db import models


class Crop(models.Model):
    """
    Static crop catalog — seeded with demo data in Phase 3/§34, read
    by the (not-yet-built) recommendation engine and by other apps
    (fertilizers, crop calendar) via crop_name lookups.
    """
    name = models.CharField(max_length=100, unique=True)
    season = models.CharField(max_length=50, blank=True)          # e.g. "Kharif", "Rabi"
    water_requirement = models.CharField(max_length=50, blank=True)
    soil_requirement = models.CharField(max_length=100, blank=True)
    growing_duration_days = models.PositiveIntegerField(null=True, blank=True)
    farming_tips = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CropRecommendation(models.Model):
    """
    One saved recommendation-request + result for a farmer. The
    `predicted_crops` field stores the ranked list returned by
    ml_models.crop_recommendation.predictor once Phase 3 implements
    it — schema intentionally loose (JSON) until that predictor's
    exact output shape is finalized.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="crop_recommendations"
    )
    # Inputs, per spec §5
    soil_type = models.CharField(max_length=50, blank=True)
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    rainfall = models.FloatField(null=True, blank=True)
    season = models.CharField(max_length=50, blank=True)
    land_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    irrigation_available = models.BooleanField(default=False)

    predicted_crops = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"CropRecommendation for {self.user} ({self.created_at:%Y-%m-%d})"
