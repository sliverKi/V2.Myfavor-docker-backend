from django.db import models
from common.models import CommonModel

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
    def __str__(self)->str:
        return f"{self.ScheduleType}"
    class Meta:
        verbose_name_plural = "Idol-Schedules"