from django.contrib import admin
from .models import Groups 

@admin.register(Groups)
class Group(admin.ModelAdmin):
    list_display=("id", "belong", "Girl_group", "Boy_group", "idol_name_kr","idol_name_en")
    list_display_links=("id", "belong", "Girl_group", "Boy_group", "idol_name_kr","idol_name_en")
    search_fields = (
        "belong",
        "Girl_group", 
        "Boy_group",
        "idol_name_kr",
        "idol_name_en",
    )
    

