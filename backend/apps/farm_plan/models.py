from django.conf import settings
from django.db import models

from apps.crops.models import Crop


class CropCalendarStage(models.Model):
    """
    Section 14: static lifecycle reference per crop — land prep,
    sowing, germination, fertilizer stage, irrigation stages, disease
    monitoring, harvest. Seeded per crop (seed_crop_calendar), and
    used as the template FarmPlan.generate_for() builds a personalized
    plan from.
    """
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="calendar_stages")
    stage_order = models.PositiveSmallIntegerField()
    stage_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    typical_week_start = models.PositiveSmallIntegerField(help_text="Week number from sowing (1-based)")
    typical_week_end = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["crop", "stage_order"]
        unique_together = ("crop", "stage_order")

    def __str__(self):
        return f"{self.crop.name} — {self.stage_name} (wk {self.typical_week_start}-{self.typical_week_end})"


class FarmPlan(models.Model):
    """
    Section 19: "My Farm Plan" — a personalized, editable, trackable
    plan generated from the farmer's profile + chosen crop. Distinct
    from the static CropCalendarStage template it was generated from;
    editing a FarmPlanTask never touches the template.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farm_plans"
    )
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    season = models.CharField(max_length=50, blank=True)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FarmPlanTask(models.Model):
    """One week's task within a FarmPlan — editable and checkable off."""
    farm_plan = models.ForeignKey(FarmPlan, on_delete=models.CASCADE, related_name="tasks")
    week_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["week_number"]

    def __str__(self):
        return f"Week {self.week_number}: {self.title}"
