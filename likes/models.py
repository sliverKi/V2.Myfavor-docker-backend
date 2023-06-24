from django.db import models
from common.models import CommonModel
class IdolLike(CommonModel):
    user=models.ForeignKey(
        "users.user",
        on_delete=models.CASCADE
    )
    idol=models.ForeignKey(
        "idols.Idol",
        on_delete=models.CASCADE,
        related_name="idolLike"
    )
    unique_together=("user","idol")