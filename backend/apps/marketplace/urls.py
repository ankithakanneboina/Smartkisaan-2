from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateDeleteView, WishlistToggleView, WishlistListView, FarmerOrdersView
urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/create/", ProductCreateView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/manage/", ProductUpdateDeleteView.as_view()),
    path("products/<int:pk>/wishlist/", WishlistToggleView.as_view()),
    path("wishlist/", WishlistListView.as_view()),
    path("farmer/orders/", FarmerOrdersView.as_view()),
]
