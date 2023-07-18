from django.db import models
from django.utils import timezone

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)