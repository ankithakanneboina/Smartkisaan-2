from django.conf import settings
from django.db import models


class Reminder(models.Model):
    """
    Section 21 (Smart Notifications) starts here as user-created and
    manually-completed reminders. Later phases (crop calendar §14,
    farm plan §19) will create these automatically instead of the
    farmer typing them by hand — same model, same API, just a
    different creator.
    """

    class ReminderType(models.TextChoices):
        WEATHER = "weather", "Weather alert"
        IRRIGATION = "irrigation", "Irrigation"
        FERTILIZER = "fertilizer", "Fertilizer"
        CROP_CALENDAR = "crop_calendar", "Crop calendar event"
        MARKET = "market", "Market price"
        DISEASE = "disease", "Disease alert"
        SCHEME = "scheme", "Government scheme"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminders"
    )
    reminder_type = models.CharField(max_length=20, choices=ReminderType.choices, default=ReminderType.OTHER)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["is_done", "due_date", "-created_at"]

    def __str__(self):
        return self.title


class NotificationPreference(models.Model):
    """
    Section 21: "Allow notification preferences." One row per farmer,
    one boolean toggle per Reminder.ReminderType. Reminder list/upcoming
    views filter out any type the farmer has turned off — the reminder
    still gets created (so re-enabling shows history), it just doesn't
    surface while disabled.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_preference"
    )
    weather_enabled = models.BooleanField(default=True)
    irrigation_enabled = models.BooleanField(default=True)
    fertilizer_enabled = models.BooleanField(default=True)
    crop_calendar_enabled = models.BooleanField(default=True)
    market_enabled = models.BooleanField(default=True)
    disease_enabled = models.BooleanField(default=True)
    scheme_enabled = models.BooleanField(default=True)

    FIELD_BY_TYPE = {
        Reminder.ReminderType.WEATHER: "weather_enabled",
        Reminder.ReminderType.IRRIGATION: "irrigation_enabled",
        Reminder.ReminderType.FERTILIZER: "fertilizer_enabled",
        Reminder.ReminderType.CROP_CALENDAR: "crop_calendar_enabled",
        Reminder.ReminderType.MARKET: "market_enabled",
        Reminder.ReminderType.DISEASE: "disease_enabled",
        Reminder.ReminderType.SCHEME: "scheme_enabled",
    }

    def enabled_types(self):
        """Reminder type values this farmer currently wants to see."""
        return [
            rtype for rtype, field in self.FIELD_BY_TYPE.items() if getattr(self, field)
        ] + [Reminder.ReminderType.OTHER]  # OTHER has no toggle, always shown

    def __str__(self):
        return f"Notification prefs for {self.user}"
