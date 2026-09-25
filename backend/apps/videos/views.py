from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Video, VideoFavorite, VideoWatchHistory
from .serializers import VideoSerializer, VideoWatchHistorySerializer


class VideoListView(generics.ListAPIView):
    """GET /api/videos/?search=&category= — §16 search + category filter."""
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Video.objects.all()

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(description__icontains=search)

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)

        return qs.distinct()

    def get_serializer_context(self):
        return {"request": self.request}


class VideoFavoriteToggleView(APIView):
    """POST /api/videos/<id>/favorite/ — toggles favorite on/off, returns new state."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        video = Video.objects.filter(pk=pk).first()
        if not video:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = VideoFavorite.objects.get_or_create(user=request.user, video=video)
        if not created:
            favorite.delete()
            return Response({"is_favorited": False})
        return Response({"is_favorited": True})


class VideoFavoriteListView(generics.ListAPIView):
    """GET /api/videos/favorites/ — the logged-in farmer's favorited videos."""
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Video.objects.filter(favorited_by__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class VideoWatchView(APIView):
    """POST /api/videos/<id>/watch/ — logs a watch event (call when playback starts)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        video = Video.objects.filter(pk=pk).first()
        if not video:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)
        VideoWatchHistory.objects.create(user=request.user, video=video)
        return Response(status=status.HTTP_201_CREATED)


class VideoWatchHistoryListView(generics.ListAPIView):
    """GET /api/videos/history/ — the logged-in farmer's watch history, most recent first."""
    serializer_class = VideoWatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoWatchHistory.objects.filter(user=self.request.user).select_related("video")
