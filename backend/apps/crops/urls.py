from django.urls import path

from .views import CropListView, CropRecommendView, CropRecommendationHistoryView

urlpatterns = [
    path("", CropListView.as_view(), name="crop-list"),
    path("recommend/", CropRecommendView.as_view(), name="crop-recommend"),
    path("recommendations/", CropRecommendationHistoryView.as_view(), name="crop-recommendation-history"),
]
