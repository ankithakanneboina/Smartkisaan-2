from rest_framework import serializers

from .models import CommunityPost, Comment, PostLike, PostReport


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "username", "content", "created_at")
        read_only_fields = ("id", "username", "created_at")


class CommunityPostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = CommunityPost
        fields = (
            "id", "username", "title", "content", "category", "image",
            "like_count", "comment_count", "is_liked", "created_at",
        )
        read_only_fields = ("id", "username", "created_at")

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context.get("request").user if self.context.get("request") else None
        if not user or not user.is_authenticated:
            return False
        return obj.likes.filter(user=user).exists()


class CommunityPostDetailSerializer(CommunityPostSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(CommunityPostSerializer.Meta):
        fields = CommunityPostSerializer.Meta.fields + ("comments",)


class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = ("id", "reason", "created_at")
        read_only_fields = ("id", "created_at")
