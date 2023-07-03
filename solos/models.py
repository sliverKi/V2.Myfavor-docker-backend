from django.db import models
from common.models import CommonModel
import datetime
class Solo(CommonModel):
    enter=models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    solo_profile=models.URLField(
        max_length=100000,
        blank=True,
        null=True,
    )
    member=models.ForeignKey(
        "idols.Idol",
        max_length=40,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="idol_solo"
    )
    solo_debut=models.DateField(default=datetime.date.today)
    solo_insta=models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
    )
    solo_youtube=models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
    )
    def __str__(self) -> str:
        return f"{self.member}"
    
    class Meta:
        verbose_name_plural = "Idols_Solo"
