from django.urls import path

from .views import (
    VideoListView,
    VideoFavoriteToggleView,
    VideoFavoriteListView,
    VideoWatchView,
    VideoWatchHistoryListView,
)

urlpatterns = [
    path("", VideoListView.as_view(), name="video-list"),
    path("favorites/", VideoFavoriteListView.as_view(), name="video-favorites"),
    path("history/", VideoWatchHistoryListView.as_view(), name="video-history"),
    path("<int:pk>/favorite/", VideoFavoriteToggleView.as_view(), name="video-favorite-toggle"),
    path("<int:pk>/watch/", VideoWatchView.as_view(), name="video-watch"),
]
