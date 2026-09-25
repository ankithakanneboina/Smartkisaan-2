from django.urls import path

from .views import DiseaseListView, DiseaseDetectionCreateView, DiseaseDetectionHistoryView

urlpatterns = [
    path("", DiseaseListView.as_view(), name="disease-list"),
    path("detect/", DiseaseDetectionCreateView.as_view(), name="disease-detect"),
    path("history/", DiseaseDetectionHistoryView.as_view(), name="disease-history"),
]
