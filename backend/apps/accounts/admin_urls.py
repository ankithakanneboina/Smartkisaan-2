from django.urls import path
from .views import AdminUserListView, AdminUserDetailView, AdminAnalyticsView

urlpatterns = [
    path("users/", AdminUserListView.as_view()),
    path("users/<int:pk>/", AdminUserDetailView.as_view()),
    path("analytics/", AdminAnalyticsView.as_view()),
]
