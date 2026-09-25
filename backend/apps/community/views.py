from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CommunityPost, Comment, PostLike, PostReport
from .serializers import (
    CommunityPostSerializer,
    CommunityPostDetailSerializer,
    CommentSerializer,
    PostReportSerializer,
)


class CommunityPostListCreateView(generics.ListCreateAPIView):
    """
    GET /api/community/posts/?search=&category=  — §18 search + category filter
    POST /api/community/posts/  (multipart: title, content, category, image)
    """
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        qs = CommunityPost.objects.select_related("user")

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(content__icontains=search)

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)

        return qs.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class CommunityPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/community/posts/<id>/ — only the author can edit/delete their own."""
    serializer_class = CommunityPostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CommunityPost.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method in ("PATCH", "PUT", "DELETE") and obj.user != request.user:
            self.permission_denied(request, message="You can only edit or delete your own posts.")


class CommentListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/community/posts/<post_id>/comments/"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs["post_id"])


class PostLikeToggleView(APIView):
    """POST /api/community/posts/<id>/like/ — toggles like, returns new state + count."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = CommunityPost.objects.filter(pk=pk).first()
        if not post:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like, created = PostLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({"is_liked": False, "like_count": post.likes.count()})
        return Response({"is_liked": True, "like_count": post.likes.count()})


class PostReportCreateView(generics.CreateAPIView):
    """POST /api/community/posts/<id>/report/ — flags a post for admin review."""
    serializer_class = PostReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = CommunityPost.objects.filter(pk=self.kwargs["pk"]).first()
        if not post:
            raise NotFound("Post not found.")
        serializer.save(post=post, reported_by=self.request.user)
