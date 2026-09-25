from dataclasses import asdict

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ml_models.fertilizer_recommendation.predictor import FertilizerRecommendationPredictor

from apps.crops.models import Crop
from .models import Fertilizer, FertilizerRecommendation
from .serializers import (
    FertilizerSerializer,
    FertilizerRecommendationRequestSerializer,
    FertilizerRecommendationSerializer,
)

_predictor = FertilizerRecommendationPredictor()


class FertilizerListView(generics.ListAPIView):
    """GET /api/fertilizers/ — the static fertilizer catalog (§34 demo data)."""
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [permissions.IsAuthenticated]


class FertilizerRecommendView(APIView):
    """
    POST /api/fertilizers/recommend/
    Runs the rule-based NPK-gap predictor, saves the request+result,
    returns ranked fertilizer recommendations with quantities.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        input_serializer = FertilizerRecommendationRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated = input_serializer.validated_data

        predictions = _predictor.predict(validated)
        predicted_fertilizers = [asdict(p) for p in predictions]

        crop_obj = None
        crop_name = validated.get("crop", "")
        if crop_name:
            crop_obj = Crop.objects.filter(name__iexact=crop_name).first()

        record = FertilizerRecommendation.objects.create(
            user=request.user,
            crop=crop_obj,
            soil_type=validated.get("soil_type", ""),
            nitrogen=validated.get("n"),
            phosphorus=validated.get("p"),
            potassium=validated.get("k"),
            ph=validated.get("ph"),
            growth_stage=validated.get("growth_stage", ""),
            land_area=validated.get("land_area"),
            predicted_fertilizers=predicted_fertilizers,
        )
        return Response(FertilizerRecommendationSerializer(record).data)


class FertilizerRecommendationHistoryView(generics.ListAPIView):
    """GET /api/fertilizers/recommendations/ — the logged-in farmer's past requests."""
    serializer_class = FertilizerRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FertilizerRecommendation.objects.filter(user=self.request.user)
