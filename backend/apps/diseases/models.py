from django.conf import settings
from django.db import models


class Disease(models.Model):
    """
    Reference catalog of known crop diseases — informational content,
    independent of whether a trained detection model exists yet.
    Populated with real agronomic reference info (§34 demo data),
    used for the "browse known diseases" view and, once a model is
    trained, to look up full detail for a predicted disease name.
    """
    name = models.CharField(max_length=150, unique=True)
    crop_name = models.CharField(max_length=100, blank=True)
    symptoms = models.TextField(blank=True)
    possible_causes = models.TextField(blank=True)
    recommended_actions = models.TextField(blank=True)
    prevention_methods = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DiseaseDetection(models.Model):
    """
    Section 8: one uploaded-image detection attempt. `status` is the
    honest signal for the frontend — while no trained model exists,
    every attempt resolves to "unavailable" rather than a fabricated
    diagnosis (see ml_models/disease_detection/README.md).
    """

    class Status(models.TextChoices):
        UNAVAILABLE = "unavailable", "Detection unavailable — no trained model yet"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Processing failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="disease_detections"
    )
    image = models.ImageField(upload_to="disease_detections/")
    crop_hint = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNAVAILABLE)
    predicted_disease = models.CharField(max_length=150, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Detection for {self.user} ({self.created_at:%Y-%m-%d})"
