from rest_framework import generics, permissions

from .models import FarmActivity
from .serializers import FarmActivitySerializer


class FarmActivityListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/farm-activities/ — the logged-in user's own activities only."""
    serializer_class = FarmActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmActivity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/farm-activities/<id>/"""
    serializer_class = FarmActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmActivity.objects.filter(user=self.request.user)


class RecentFarmActivityView(generics.ListAPIView):
    """GET /api/farm-activities/recent/ — last 5, for the dashboard card."""
    serializer_class = FarmActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmActivity.objects.filter(user=self.request.user)[:5]
