from django.urls import path

from .views import MarketPriceListView, MarketPriceTrendView

urlpatterns = [
    path("prices/", MarketPriceListView.as_view(), name="market-price-list"),
    path("prices/trend/", MarketPriceTrendView.as_view(), name="market-price-trend"),
]
