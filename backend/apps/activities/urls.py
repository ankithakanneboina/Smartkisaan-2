from django.urls import path

from .views import FarmActivityListCreateView, FarmActivityDetailView, RecentFarmActivityView

urlpatterns = [
    path("", FarmActivityListCreateView.as_view(), name="activity-list-create"),
    path("recent/", RecentFarmActivityView.as_view(), name="activity-recent"),
    path("<int:pk>/", FarmActivityDetailView.as_view(), name="activity-detail"),
]
