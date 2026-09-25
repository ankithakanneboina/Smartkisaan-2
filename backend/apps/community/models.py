from django.conf import settings
from django.db import models


class CommunityPost(models.Model):
    """Section 18: a farmer's forum post/question, with an optional image."""

    class Category(models.TextChoices):
        CROPS = "crops", "Crops"
        DISEASES = "diseases", "Diseases"
        FERTILIZERS = "fertilizers", "Fertilizers"
        WEATHER = "weather", "Weather"
        MARKETS = "markets", "Markets"
        GOVERNMENT_SCHEMES = "government_schemes", "Government schemes"
        GENERAL = "general", "General farming"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="community_posts"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.GENERAL)
    image = models.ImageField(upload_to="community_posts/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="community_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class PostLike(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="community_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")


class PostReport(models.Model):
    """
    Moderation: a farmer flags a post as inappropriate/spam/etc.
    Admin reviews reports via /admin/ — no automatic takedown, per
    the spec's "moderation/report functionality" (report, not auto-remove).
    """
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="community_reports"
    )
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("post", "reported_by")
