from rest_framework import serializers

from .models import FarmerProfile


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = (
            "id",
            "profile_photo",
            "full_name",
            "mobile_number",
            "location",
            "district",
            "state",
            "land_area_acres",
            "soil_type",
            "irrigation_type",
            "crops_grown",
            "preferred_language",
            "created_at",
            "updated_at",
            # latitude/longitude intentionally excluded — this endpoint
            # is the farmer's own record but precise coordinates stay
            # off the general-purpose serializer; a separate, narrowly
            # scoped endpoint handles map features in Phase 8.
        )
        read_only_fields = ("id", "created_at", "updated_at")
