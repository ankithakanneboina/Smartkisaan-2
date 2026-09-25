from django.contrib import admin

from .models import FarmerProfile


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "district", "state", "soil_type", "irrigation_type")
    list_filter = ("state", "soil_type", "irrigation_type")
    search_fields = ("full_name", "user__email", "district", "state")
