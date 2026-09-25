from rest_framework import serializers

from .models import Video, VideoFavorite, VideoWatchHistory


class VideoSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            "id", "title", "description", "category",
            "video_url", "thumbnail_url", "is_favorited", "created_at",
        )

    def get_is_favorited(self, obj):
        user = self.context.get("request").user if self.context.get("request") else None
        if not user or not user.is_authenticated:
            return False
        # Prefetched as `_favorited_by_user` when the view annotates it;
        # falls back to a query if not (e.g. detail view).
        if hasattr(obj, "_favorited_by_user"):
            return obj._favorited_by_user
        return VideoFavorite.objects.filter(user=user, video=obj).exists()


class VideoWatchHistorySerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)

    class Meta:
        model = VideoWatchHistory
        fields = ("id", "video", "watched_at")
