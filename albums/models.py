from django.db import models
import datetime

class Album(models.Model):
    solo_artists=models.ForeignKey(
        "idols.Idol",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="albums"
    )
    group_artists=models.ForeignKey(
        "groups.Group",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="albums"
    )
    album_name=models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    album_cover=models.URLField(
        max_length=100000,
        blank=True,
        null=True,
    )
    release_date=models.DateField(
        default=datetime.date.today
    )

    def __str__ (self)->str:
        return f"{self.album_name}"
