from django.contrib import admin

from .models import CropCalendarStage, FarmPlan, FarmPlanTask


@admin.register(CropCalendarStage)
class CropCalendarStageAdmin(admin.ModelAdmin):
    list_display = ("crop", "stage_order", "stage_name", "typical_week_start", "typical_week_end")
    list_filter = ("crop",)


class FarmPlanTaskInline(admin.TabularInline):
    model = FarmPlanTask
    extra = 0


@admin.register(FarmPlan)
class FarmPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "crop", "status", "start_date")
    list_filter = ("status",)
    inlines = [FarmPlanTaskInline]
