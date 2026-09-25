from django.urls import path

from .views import MyFarmerProfileView

urlpatterns = [
    path("me/", MyFarmerProfileView.as_view(), name="farmer-profile-me"),
]
