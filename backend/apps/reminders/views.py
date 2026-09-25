from rest_framework import generics, permissions

from .models import Reminder, NotificationPreference
from .serializers import ReminderSerializer, NotificationPreferenceSerializer


def _visible_types(user):
    """Reminder types this user currently wants surfaced, per their preferences."""
    prefs, _ = NotificationPreference.objects.get_or_create(user=user)
    return prefs.enabled_types()


class ReminderListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/reminders/ — GET respects notification preferences."""
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(
            user=self.request.user, reminder_type__in=_visible_types(self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/reminders/<id>/ — PATCH is_done to check it off."""
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)


class UpcomingReminderView(generics.ListAPIView):
    """GET /api/reminders/upcoming/ — not-done, soonest-first, for the dashboard card. Respects preferences."""
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(
            user=self.request.user, is_done=False, reminder_type__in=_visible_types(self.request.user)
        )[:5]


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/reminders/preferences/
    Creates default (all-on) preferences on first GET, same pattern
    as apps.farmers.MyFarmerProfileView.
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        prefs, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return prefs
