from django.contrib import admin
from .models import Idol

@admin.register(Idol)
class Idols(admin.ModelAdmin):
    list_display = ("pk", "idol_name_kr","idol_name_en")
    list_display_links = (
        "pk",
        "idol_name_kr",
        "idol_name_en"
    )
    search_fields = (
        "idol_name_kr",
        "idol_name_en",
    )
    

