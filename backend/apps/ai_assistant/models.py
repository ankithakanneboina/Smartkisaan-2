from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    """
    Section 6/7: one turn of the AI Farming Assistant conversation.
    Stores both the farmer's question and the structured answer, so
    /api/ai/history/ can render a real chat thread, and so switching
    providers later (rule-based → real LLM) doesn't lose past history
    since the stored shape (structured_response) stays the same.
    """

    class Language(models.TextChoices):
        ENGLISH = "en", "English"
        TELUGU = "te", "Telugu"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_chat_messages"
    )
    language = models.CharField(max_length=5, choices=Language.choices, default=Language.ENGLISH)
    question = models.TextField()

    # Structured per §6: problem / possible_cause / recommended_action /
    # precautions / when_to_contact_expert — see services/base.py.
    structured_response = models.JSONField(default=dict, blank=True)
    provider = models.CharField(max_length=30, default="rule_based")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} — {self.question[:40]}"
