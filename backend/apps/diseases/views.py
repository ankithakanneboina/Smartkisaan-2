from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from ml_models.disease_detection.predictor import DiseaseDetectionPredictor

from .models import Disease, DiseaseDetection
from .serializers import DiseaseSerializer, DiseaseDetectionSerializer

_predictor = DiseaseDetectionPredictor()


class DiseaseListView(generics.ListAPIView):
    """GET /api/diseases/ — reference catalog of known diseases (§34 demo data)."""
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.IsAuthenticated]


class DiseaseDetectionCreateView(generics.CreateAPIView):
    """
    POST /api/diseases/detect/  (multipart: image, crop_hint)
    Validates and stores the upload, then calls the ML service
    abstraction. While no trained model exists, this always resolves
    to status="unavailable" — see ml_models/disease_detection/predictor.py.
    Never fabricates a diagnosis (§8 requirement).
    """
    serializer_class = DiseaseDetectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        detection = serializer.save(user=self.request.user, status=DiseaseDetection.Status.UNAVAILABLE)

        if _predictor.is_ready():
            try:
                results = _predictor.predict({
                    "image_path": detection.image.path,
                    "crop": detection.crop_hint,
                })
                if results:
                    top = results[0]
                    detection.status = DiseaseDetection.Status.SUCCESS
                    detection.predicted_disease = top.label
                    detection.confidence = top.confidence
                    detection.save()
            except Exception:
                detection.status = DiseaseDetection.Status.FAILED
                detection.save()
        # else: predictor not ready — record stays "unavailable", which
        # is the honest, expected state until Phase 5's model is trained.


class DiseaseDetectionHistoryView(generics.ListAPIView):
    """GET /api/diseases/history/ — the logged-in farmer's past detection attempts."""
    serializer_class = DiseaseDetectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DiseaseDetection.objects.filter(user=self.request.user)
