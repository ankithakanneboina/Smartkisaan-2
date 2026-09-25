from rest_framework import serializers

from .models import Disease, DiseaseDetection

MAX_IMAGE_SIZE_MB = 5
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = (
            "id", "name", "crop_name", "symptoms",
            "possible_causes", "recommended_actions", "prevention_methods",
        )


class DiseaseDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseDetection
        fields = (
            "id", "image", "crop_hint", "status",
            "predicted_disease", "confidence", "created_at",
        )
        read_only_fields = ("id", "status", "predicted_disease", "confidence", "created_at")

    def validate_image(self, image):
        # §27: image validation, file-size validation.
        if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Image must be under {MAX_IMAGE_SIZE_MB}MB.")
        content_type = getattr(image, "content_type", None)
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError("Only JPEG, PNG, or WEBP images are supported.")
        return image
