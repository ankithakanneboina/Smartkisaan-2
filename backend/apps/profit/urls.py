from django.urls import path

from .views import ProfitCalculateView, ProfitCalculationHistoryView

urlpatterns = [
    path("calculate/", ProfitCalculateView.as_view(), name="profit-calculate"),
    path("history/", ProfitCalculationHistoryView.as_view(), name="profit-history"),
]
