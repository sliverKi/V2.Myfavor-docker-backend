from django.contrib import admin
from .models import Prize
# Register your models here.
@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display=("prize_name","date")
    list_display_link=("prize_name","date") 
    
