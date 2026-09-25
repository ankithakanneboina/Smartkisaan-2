from django.contrib import admin

from .models import CommunityPost, Comment, PostLike, PostReport


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "content", "user__email")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")


@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ("post", "reported_by", "reason", "reviewed", "created_at")
    list_filter = ("reviewed",)
    actions = ["mark_reviewed"]

    def mark_reviewed(self, request, queryset):
        queryset.update(reviewed=True)
    mark_reviewed.short_description = "Mark selected reports as reviewed"
