from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Report

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def thumbnail(self, object):
        try:
            return format_html(
                '<img src="{}" width="40" style="border-radius:50%"/>'.format(
                    object.profileImg.url,
                )
            )
        except:
            pass

    thumbnail.short_description = "profileImg"
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "name",
                    "profileImg",
                    "nickname",
                    "email",
                    "phone",
                    "pick",
                    "age",
                    "is_admin",
                    "is_active"
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = (
        "id",
        "name",
        "nickname",
        "email",
        "phone",
        "pick",
        "is_admin",
        "is_active"
    )
    list_display_links = (
        "email",
        "phone",
        "nickname",
        "name",
        "pick",
    )
    list_filter = ("nickname","is_active")
    search_fields = (
        "name",
        "nickname",
        "name",
        "pick",
    )
    ordering = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "email", "nickname", "password1", "password2"),
            },
        ),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "ScheduleTitle",
        "location",
        "is_enroll",
    )
    list_display_links = (
        "pk",
        "ScheduleTitle",
        "location",
    )