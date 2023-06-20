from django.contrib import admin
from .models import Schedule
# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "ScheduleTitle",
        "ScheduleType",
        "when",
    )
    list_display_links = (
        "pk",
        "ScheduleTitle",
        "ScheduleType"
    
    )

    # readonly_fields = (
    #     "created_at",
    #     "updated_at",
    # )