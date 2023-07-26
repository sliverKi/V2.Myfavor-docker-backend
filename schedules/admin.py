from django.contrib import admin
from .models import Schedule
# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "owner",
        "ScheduleTitle",
        "ScheduleType",
        "when",
    )
    list_display_links = (
        "pk",
        "owner",
        "ScheduleTitle",
        "ScheduleType"
    )

    # readonly_fields = (
    #     "created_at",
    #     "updated_at",
    # )