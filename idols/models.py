from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from common.models import CommonModel
import datetime
from prizes.models import Prize
# from times.models import TimeModel
class Idol(models.Model):
    """Idol Model Definition"""
    idol_name_kr = models.CharField(max_length=100, default="")
    idol_name_en = models.CharField(max_length=100, default="")

    idol_profile = models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
        #validators=[URLValidator( "유효한 URL을 입력하세요. ")]
    )
    is_solo = models.BooleanField(default=False)#False==Group, True==Solo

    group=models.ManyToManyField(
        "groups.Group",
        blank=True,
        null=True,
        related_name="idols"
    )
    idol_birthday = models.DateField(default=datetime.date.today)

    has_schedules=models.BooleanField(default=False)#true: 잇, False; 없
    idol_schedules = models.ManyToManyField(
        "schedules.Schedule",
        blank=True,
        related_name="idols",
    )  
    pickCount=models.PositiveBigIntegerField( #user's pick
        default=0,
        editable=False,
    )   

    def __str__(self)->str:
        return f"{self.idol_name_kr} ( {self.idol_name_en} )"

    class Meta:
        verbose_name_plural = "Our_Idols"



