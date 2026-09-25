from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.crops.models import CropRecommendation
from apps.fertilizers.models import FertilizerRecommendation
from apps.diseases.models import DiseaseDetection
from apps.ai_assistant.models import ChatMessage
from apps.profit.models import ProfitCalculation
from apps.farm_plan.models import FarmPlan

User = get_user_model()


class AnalyticsSummaryView(APIView):
    """
    GET /api/analytics/summary/
    Section 24: admin dashboard aggregates — total/active farmers,
    popular crops, most-used features, disease detection usage,
    recommendation usage. Read-only aggregation over existing data;
    no separate analytics-tracking model needed since every feature
    already persists its own usage records (recommendations, chat
    messages, detections, etc.) that this view just counts.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # FarmerProfile is created lazily (first profile-page visit),
        # so it undercounts registered users — User is the true signup
        # count. Excludes staff/admin accounts from the farmer count.
        total_farmers = User.objects.filter(is_staff=False).count()
        active_farmers = User.objects.filter(
            is_staff=False, last_login__gte=thirty_days_ago
        ).count()

        popular_crops = list(
            FarmPlan.objects.exclude(crop__isnull=True)
            .values("crop__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        feature_usage = {
            "crop_recommendations": CropRecommendation.objects.count(),
            "fertilizer_recommendations": FertilizerRecommendation.objects.count(),
            "disease_detections": DiseaseDetection.objects.count(),
            "ai_chat_messages": ChatMessage.objects.count(),
            "profit_calculations": ProfitCalculation.objects.count(),
            "farm_plans_generated": FarmPlan.objects.count(),
        }
        most_used_features = sorted(feature_usage.items(), key=lambda kv: kv[1], reverse=True)

        disease_detection_by_status = list(
            DiseaseDetection.objects.values("status").annotate(count=Count("id")).order_by("-count")
        )

        return Response({
            "total_farmers": total_farmers,
            "active_farmers_last_30_days": active_farmers,
            "popular_crops": [
                {"crop": row["crop__name"], "farm_plans": row["count"]} for row in popular_crops
            ],
            "most_used_features": [
                {"feature": name, "count": count} for name, count in most_used_features
            ],
            "disease_detection_usage": {
                "total": DiseaseDetection.objects.count(),
                "by_status": disease_detection_by_status,
            },
            "recommendation_usage": {
                "crop_recommendations": CropRecommendation.objects.count(),
                "fertilizer_recommendations": FertilizerRecommendation.objects.count(),
            },
        })
