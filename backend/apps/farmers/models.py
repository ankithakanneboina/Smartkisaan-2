from django.conf import settings
from django.db import models


class FarmerProfile(models.Model):
    """
    Optional 1:1 extension of User with farming-specific data.
    Referenced by nearly every later app (crops, fertilizers,
    diseases, farm-plan, activity-tracker, notifications, ...),
    so it's built in Phase 1 alongside auth even though the
    dashboard that displays it comes in Phase 2.
    """

    class SoilType(models.TextChoices):
        ALLUVIAL = "alluvial", "Alluvial"
        BLACK = "black", "Black (Regur)"
        RED = "red", "Red"
        LATERITE = "laterite", "Laterite"
        SANDY = "sandy", "Sandy"
        CLAY = "clay", "Clay"
        LOAMY = "loamy", "Loamy"

    class IrrigationType(models.TextChoices):
        RAINFED = "rainfed", "Rain-fed"
        CANAL = "canal", "Canal"
        BOREWELL = "borewell", "Borewell"
        DRIP = "drip", "Drip"
        SPRINKLER = "sprinkler", "Sprinkler"

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        TELUGU = "te", "Telugu"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farmer_profile"
    )
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    land_area_acres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    soil_type = models.CharField(max_length=20, choices=SoilType.choices, blank=True)
    irrigation_type = models.CharField(max_length=20, choices=IrrigationType.choices, blank=True)
    crops_grown = models.JSONField(default=list, blank=True)  # e.g. ["rice", "cotton"]
    preferred_language = models.CharField(
        max_length=5, choices=Language.choices, default=Language.ENGLISH
    )
    # Precise coordinates kept off the public API surface (see serializer) —
    # section 23 requires private farmer location not be exposed publicly.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.email
