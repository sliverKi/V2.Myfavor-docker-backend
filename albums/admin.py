from django.contrib import admin
from .models import Album

@admin.register(Album)
class Album(admin.ModelAdmin):
    list_display=("id", "release_date","album_name")
    list_display_links=("id", "release_date","album_name")
    search_fields = (
        "enter", 
        "group_artists",
        "album_name"
    )