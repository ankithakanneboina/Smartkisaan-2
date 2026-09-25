from django.urls import path

from .views import FertilizerListView, FertilizerRecommendView, FertilizerRecommendationHistoryView

urlpatterns = [
    path("", FertilizerListView.as_view(), name="fertilizer-list"),
    path("recommend/", FertilizerRecommendView.as_view(), name="fertilizer-recommend"),
    path("recommendations/", FertilizerRecommendationHistoryView.as_view(), name="fertilizer-recommendation-history"),
]
