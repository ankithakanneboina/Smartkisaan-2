from django.contrib import admin

from .models import Reminder, NotificationPreference


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "reminder_type", "due_date", "is_done")
    list_filter = ("reminder_type", "is_done")
    search_fields = ("title", "user__email")


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "weather_enabled", "irrigation_enabled", "fertilizer_enabled", "crop_calendar_enabled")
