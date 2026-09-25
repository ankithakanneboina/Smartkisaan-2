from django.conf import settings
from django.db import models


class FarmActivity(models.Model):
    """
    Section 20: farmer-logged events (sowing, irrigation, fertilizer,
    pest observation, harvest, expense). Powers the dashboard's
    "Recent farming activities" card and, later, the activity timeline
    view and FarmPlan progress tracking.
    """

    class ActivityType(models.TextChoices):
        SOWING = "sowing", "Sowing"
        IRRIGATION = "irrigation", "Irrigation"
        FERTILIZER = "fertilizer", "Fertilizer application"
        PEST_OBSERVATION = "pest_observation", "Pest/disease observation"
        HARVEST = "harvest", "Harvest"
        EXPENSE = "expense", "Expense"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farm_activities"
    )
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    crop_name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    # Only populated for activity_type == "expense"; kept generic (no FK to
    # a specific cost category yet) since the profit calculator (Phase 7)
    # is what will define categories properly.
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activity_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-activity_date", "-created_at"]

    def __str__(self):
        return f"{self.get_activity_type_display()} — {self.crop_name or 'general'} ({self.activity_date})"
