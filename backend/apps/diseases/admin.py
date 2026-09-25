from django.contrib import admin

from .models import Disease, DiseaseDetection


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name", "crop_name")
    search_fields = ("name", "crop_name")


@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = ("user", "crop_hint", "status", "predicted_disease", "created_at")
    list_filter = ("status",)
