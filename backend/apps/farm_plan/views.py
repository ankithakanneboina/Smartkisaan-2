from datetime import timedelta

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.crops.models import Crop
from apps.reminders.models import Reminder

from .models import CropCalendarStage, FarmPlan, FarmPlanTask
from .serializers import (
    CropCalendarStageSerializer,
    FarmPlanSerializer,
    FarmPlanTaskSerializer,
    GeneratePlanRequestSerializer,
)


class CropCalendarView(generics.ListAPIView):
    """
    GET /api/farm-plan/calendar/?crop=<name>
    Section 14: the static lifecycle stages for a crop (land prep →
    sowing → germination → fertilizer → irrigation → disease
    monitoring → harvest), read-only reference data.
    """
    serializer_class = CropCalendarStageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        crop_name = self.request.query_params.get("crop")
        qs = CropCalendarStage.objects.select_related("crop")
        if crop_name:
            qs = qs.filter(crop__name__iexact=crop_name)
        return qs


class GenerateFarmPlanView(APIView):
    """
    POST /api/farm-plan/generate/
    Section 19: builds a personalized, editable FarmPlan from the
    crop's CropCalendarStage template + the farmer's chosen start
    date. This is template expansion, not a predictor — transparent
    and inspectable, matching the pattern used elsewhere in this
    codebase for anything not backed by a trained model.
    Optionally creates a Reminder per task (§21 tie-in) so calendar
    events show up in the existing Reminders card without a second
    notification system.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        input_serializer = GeneratePlanRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        v = input_serializer.validated_data

        crop = Crop.objects.filter(name__iexact=v["crop"]).first()
        if not crop:
            return Response({"detail": f"No crop calendar found for '{v['crop']}'."}, status=400)

        stages = list(crop.calendar_stages.all())
        if not stages:
            return Response(
                {"detail": f"No calendar stages seeded yet for '{crop.name}'. Run seed_crop_calendar."},
                status=400,
            )

        plan = FarmPlan.objects.create(
            user=request.user,
            crop=crop,
            title=f"{crop.name} plan starting {v['start_date']}",
            season=v.get("season", ""),
            start_date=v["start_date"],
        )

        for stage in stages:
            due_date = v["start_date"] + timedelta(weeks=stage.typical_week_start - 1)
            task = FarmPlanTask.objects.create(
                farm_plan=plan,
                week_number=stage.typical_week_start,
                title=stage.stage_name,
                description=stage.description,
                due_date=due_date,
            )
            if v.get("create_reminders", True):
                Reminder.objects.create(
                    user=request.user,
                    reminder_type=Reminder.ReminderType.CROP_CALENDAR,
                    title=f"{crop.name}: {stage.stage_name}",
                    message=stage.description,
                    due_date=due_date,
                )

        return Response(FarmPlanSerializer(plan).data, status=201)


class FarmPlanListView(generics.ListAPIView):
    """GET /api/farm-plan/plans/ — the logged-in farmer's saved plans."""
    serializer_class = FarmPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmPlan.objects.filter(user=self.request.user)


class FarmPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/farm-plan/plans/<id>/ — e.g. PATCH status to 'completed'."""
    serializer_class = FarmPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmPlan.objects.filter(user=self.request.user)


class FarmPlanTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/farm-plan/tasks/<id>/ — edit or check off a single task."""
    serializer_class = FarmPlanTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FarmPlanTask.objects.filter(farm_plan__user=self.request.user)
