from dataclasses import asdict

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ml_models.crop_recommendation.predictor import CropRecommendationPredictor

from .models import Crop, CropRecommendation
from .serializers import (
    CropSerializer,
    CropRecommendationRequestSerializer,
    CropRecommendationSerializer,
)

_predictor = CropRecommendationPredictor()  # stateless rule-based scorer — safe to share


class CropListView(generics.ListAPIView):
    """GET /api/crops/ — the static crop catalog (§34 demo data)."""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated]


class CropRecommendView(APIView):
    """
    POST /api/crops/recommend/
    Runs the rule-based predictor over the farmer's soil/climate
    inputs, saves the request+result, and returns ranked crops.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        input_serializer = CropRecommendationRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated = input_serializer.validated_data

        predictions = _predictor.predict(validated)
        predicted_crops = [asdict(p) for p in predictions]

        record = CropRecommendation.objects.create(
            user=request.user,
            soil_type=validated.get("soil_type", ""),
            nitrogen=validated.get("n"),
            phosphorus=validated.get("p"),
            potassium=validated.get("k"),
            ph=validated.get("ph"),
            temperature=validated.get("temperature"),
            humidity=validated.get("humidity"),
            rainfall=validated.get("rainfall"),
            season=validated.get("season", ""),
            land_area=validated.get("land_area"),
            irrigation_available=validated.get("irrigation_available", False),
            predicted_crops=predicted_crops,
        )
        return Response(CropRecommendationSerializer(record).data)


class CropRecommendationHistoryView(generics.ListAPIView):
    """GET /api/crops/recommendations/ — the logged-in farmer's past requests."""
    serializer_class = CropRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CropRecommendation.objects.filter(user=self.request.user)
