from django.db import models
from common.models import CommonModel

class Groups(models.Model):
 
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
        related_name="groups_idol"
    )
    
    def __str__(self)->str:
        return f"{self.member}"

    class Meta:
        verbose_name_plural = "Idols_Group"

