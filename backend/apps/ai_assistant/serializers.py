from rest_framework import serializers

from .models import ChatMessage


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    language = serializers.ChoiceField(choices=ChatMessage.Language.choices, default="en")


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "language", "question", "structured_response", "provider", "created_at")
        read_only_fields = fields
