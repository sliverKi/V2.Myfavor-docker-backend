
from django.contrib import admin
from .models import Board

# Register your models here.
@admin.register(Board)
class BoardsAdmin(admin.ModelAdmin):
    list_display = ("pk", "type",)# "content")
    list_display_links = ("pk", "type",)# "content")
    search_fields = ("type",)
    list_filter = ("type",)