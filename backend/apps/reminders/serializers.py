from rest_framework import serializers

from .models import Reminder, NotificationPreference


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ("id", "reminder_type", "title", "message", "due_date", "is_done", "created_at")
        read_only_fields = ("id", "created_at")


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = (
            "weather_enabled", "irrigation_enabled", "fertilizer_enabled",
            "crop_calendar_enabled", "market_enabled", "disease_enabled", "scheme_enabled",
        )
