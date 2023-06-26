from django.db import models
from common.models import CommonModel
import datetime
class Group(models.Model):
 
    enter=models.CharField(#소속사
        max_length=40,
        blank=True,
        null=True,
    )
    groupname = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    group_profile = models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
    )
    member = models.ManyToManyField(
        "idols.Idol",
        null=True,
        related_name="groups"
    )
    group_debut=models.DateField(default=datetime.date.today)
    group_insta=models.URLField( 
        max_length=10000, 
        blank=True, 
        null=True,
    )
    group_youtube=models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
    )
  
    def __str__(self)->str:
        return f"{self.groupname}"

    class Meta:
        verbose_name_plural = "Idols_Group"

