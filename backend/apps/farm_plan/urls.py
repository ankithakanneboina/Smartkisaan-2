from django.urls import path

from .views import (
    CropCalendarView,
    GenerateFarmPlanView,
    FarmPlanListView,
    FarmPlanDetailView,
    FarmPlanTaskDetailView,
)

urlpatterns = [
    path("calendar/", CropCalendarView.as_view(), name="crop-calendar"),
    path("generate/", GenerateFarmPlanView.as_view(), name="farm-plan-generate"),
    path("plans/", FarmPlanListView.as_view(), name="farm-plan-list"),
    path("plans/<int:pk>/", FarmPlanDetailView.as_view(), name="farm-plan-detail"),
    path("tasks/<int:pk>/", FarmPlanTaskDetailView.as_view(), name="farm-plan-task-detail"),
]
