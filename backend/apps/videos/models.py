from django.conf import settings
from django.db import models


class Video(models.Model):
    """
    Section 16: admin-managed video library entry. `video_url` points
    to an externally-hosted video (YouTube etc.) — this app never
    hosts video files itself.
    """

    class Category(models.TextChoices):
        CROP_FARMING = "crop_farming", "Crop farming"
        ORGANIC_FARMING = "organic_farming", "Organic farming"
        FERTILIZERS = "fertilizers", "Fertilizers"
        IRRIGATION = "irrigation", "Irrigation"
        PEST_MANAGEMENT = "pest_management", "Pest management"
        MODERN_FARMING = "modern_farming", "Modern farming"
        GOVERNMENT_SCHEMES = "government_schemes", "Government schemes"
        MACHINERY = "machinery", "Machinery"
        SOIL_MANAGEMENT = "soil_management", "Soil management"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=Category.choices)
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class VideoFavorite(models.Model):
    """One farmer's saved/favorited video."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="video_favorites"
    )
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "video")


class VideoWatchHistory(models.Model):
    """
    One watch event. Multiple rows per user+video are allowed (each
    watch is logged), so /history/ can show recency accurately.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="video_watch_history"
    )
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch_events")
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-watched_at"]
