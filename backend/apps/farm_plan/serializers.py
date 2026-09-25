from rest_framework import serializers

from .models import CropCalendarStage, FarmPlan, FarmPlanTask


class CropCalendarStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropCalendarStage
        fields = ("id", "stage_order", "stage_name", "description", "typical_week_start", "typical_week_end")


class FarmPlanTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmPlanTask
        fields = ("id", "week_number", "title", "description", "due_date", "is_done")
        read_only_fields = ("id",)


class FarmPlanSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source="crop.name", read_only=True, default=None)
    tasks = FarmPlanTaskSerializer(many=True, read_only=True)

    class Meta:
        model = FarmPlan
        fields = ("id", "crop", "crop_name", "title", "season", "start_date", "status", "tasks", "created_at")
        read_only_fields = ("id", "created_at")


class GeneratePlanRequestSerializer(serializers.Serializer):
    crop = serializers.CharField()
    season = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField()
    create_reminders = serializers.BooleanField(required=False, default=True)
