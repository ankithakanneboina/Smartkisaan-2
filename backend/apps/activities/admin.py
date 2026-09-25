from django.contrib import admin

from .models import FarmActivity


@admin.register(FarmActivity)
class FarmActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_type", "crop_name", "activity_date")
    list_filter = ("activity_type",)
    search_fields = ("user__email", "crop_name")
