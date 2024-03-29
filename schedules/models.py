from django.db import models
from common.models import CommonModel
# from categories.models import Category
class Schedule(CommonModel):
    """Schedule Model Definition"""
    owner = models.ForeignKey(  
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    ScheduleTitle = models.CharField(
        max_length=150,
        default="",
    )
    ScheduleType = models.ForeignKey(
        "boards.Board",
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
        return f"{self.ScheduleTitle}"
    class Meta:
        verbose_name_plural = "Idol-Schedules"