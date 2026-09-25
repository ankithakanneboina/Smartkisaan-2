from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "question", "provider", "created_at")
    list_filter = ("language", "provider")
    search_fields = ("user__email", "question")
