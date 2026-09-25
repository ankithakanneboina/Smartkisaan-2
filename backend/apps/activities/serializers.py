from rest_framework import serializers

from .models import FarmActivity


class FarmActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmActivity
        fields = (
            "id",
            "activity_type",
            "crop_name",
            "notes",
            "amount",
            "activity_date",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
