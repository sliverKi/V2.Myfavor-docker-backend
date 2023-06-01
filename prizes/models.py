from django.db import models
import datetime

class Prize(models.Model):
     
    idol_name=models.ManyToManyField(
        "idols.Idol",
        related_name="prize_idol",
        blank=True,
    )
    prize_name=models.CharField(
        max_length=200,
        default="",
        blank=True,
        null=True,
    )
    date=models.DateField(
       default=datetime.date.today
    )

    def __str__(self)->str:
        return f"{self.prize_name}"
    class Meta:
        verbose_name_plural = "Prizes"