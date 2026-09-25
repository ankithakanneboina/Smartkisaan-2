from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.farmers.models import FarmerProfile

from .models import ChatMessage
from .serializers import ChatRequestSerializer, ChatMessageSerializer
from .services.service import get_ai_provider


class ChatView(APIView):
    """
    POST /api/ai/chat/  body: {"message": "...", "language": "en"|"te"}
    Runs the configured provider (rule-based by default), saves the
    turn, and returns the structured Problem/Cause/Action/Precautions/
    Expert response required by §6.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        input_serializer = ChatRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        v = input_serializer.validated_data

        # Context-aware: pass along what we know about the farmer (§6)
        # so a real LLM provider can personalize; the rule-based
        # provider ignores context today but the shape is ready.
        profile = FarmerProfile.objects.filter(user=request.user).first()
        context = {}
        if profile:
            context = {
                "crops_grown": profile.crops_grown,
                "soil_type": profile.soil_type,
                "location": profile.location,
            }

        provider = get_ai_provider()
        answer = provider.respond(question=v["message"], language=v["language"], context=context)

        message = ChatMessage.objects.create(
            user=request.user,
            language=v["language"],
            question=v["message"],
            structured_response=answer,
            provider=answer.get("provider", "rule_based"),
        )
        return Response(ChatMessageSerializer(message).data)


class ChatHistoryView(generics.ListAPIView):
    """GET /api/ai/history/ — the logged-in farmer's chat thread."""
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)
