from django.urls import path

from .views import (
    CommunityPostListCreateView,
    CommunityPostDetailView,
    CommentListCreateView,
    PostLikeToggleView,
    PostReportCreateView,
)

urlpatterns = [
    path("posts/", CommunityPostListCreateView.as_view(), name="community-post-list-create"),
    path("posts/<int:pk>/", CommunityPostDetailView.as_view(), name="community-post-detail"),
    path("posts/<int:post_id>/comments/", CommentListCreateView.as_view(), name="community-comment-list-create"),
    path("posts/<int:pk>/like/", PostLikeToggleView.as_view(), name="community-post-like-toggle"),
    path("posts/<int:pk>/report/", PostReportCreateView.as_view(), name="community-post-report"),
]
