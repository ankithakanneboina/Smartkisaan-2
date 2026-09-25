from django.urls import path

from .views import ReminderListCreateView, ReminderDetailView, UpcomingReminderView, NotificationPreferenceView

urlpatterns = [
    path("", ReminderListCreateView.as_view(), name="reminder-list-create"),
    path("upcoming/", UpcomingReminderView.as_view(), name="reminder-upcoming"),
    path("preferences/", NotificationPreferenceView.as_view(), name="reminder-preferences"),
    path("<int:pk>/", ReminderDetailView.as_view(), name="reminder-detail"),
]
