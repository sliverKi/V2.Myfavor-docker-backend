from django.contrib import admin
from .models import Group

@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display=("id", "enter", "groupname")
    list_display_links=("id", "enter", "groupname")
    search_fields = (
        "enter", 
        "groupName",
    )
    

