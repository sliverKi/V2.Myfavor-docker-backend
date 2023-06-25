from django.contrib import admin
from .models import Solo

@admin.register(Solo)
class Solo(admin.ModelAdmin):
    list_display=("id", "enter", "member")
    list_display_links=("id", "enter", "member")
    search_fields = (
        "enter", 
        "member",
    )
    