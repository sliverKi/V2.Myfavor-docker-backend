from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from common.models import CommonModel
import datetime
# from times.models import TimeModel


class Idol(models.Model):
    """Idol Model Definition"""

    class GenderChoices(models.TextChoices):
        Woman = ("Woman", "Woman")
        Man = ("Man", "Man")

    idol_name_kr = models.CharField(max_length=100, default="")
    idol_name_en = models.CharField(max_length=100, default="")
    idol_profile = models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
        #validators=[URLValidator( "유효한 URL을 입력하세요. ")]
    )

    idol_anniv = models.DateField(default=datetime.date.today)
    idol_birthday = models.DateField()

    idol_gender = models.CharField(
        max_length=8,
        choices=GenderChoices.choices,
    )

    idol_schedules = models.ManyToManyField(
        "idols.Schedule",
        blank=True,
        related_name="idols",
    )

    def __str__(self)->str:
        return f"{self.idol_name_kr}"

    class Meta:
        verbose_name_plural = "Our_Idols"


class Schedule(CommonModel):
    """Schedule Model Definition"""

    ScheduleTitle = models.CharField(
        max_length=150,
        default="",
    )
    ScheduleType = models.ForeignKey(
        "categories.Category",
        max_length=150,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="schedules",
    )
    location=models.CharField(
        max_length=150,
        default=""
    )
    participant = models.ManyToManyField(
        "idols.Idol",
        max_length=150,
        blank=True,
        related_name="schedules",
    )
    
    
    when=models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
        )

    class Meta:
        verbose_name_plural = "Idol-Schedules"
