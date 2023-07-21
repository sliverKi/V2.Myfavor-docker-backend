from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractUser,
)
from datetime import datetime
from .manager import CustomUserManager
from common.models import CommonModel

# superuser
# myfavor@gmail.com / myfavor
class User(AbstractUser):
    username = None
    name = models.CharField(
        max_length=100,
        blank=False,
        validators=[MinLengthValidator(2, "이름은 2자 이상이어야 합니다.")],
    )
    nickname = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        validators=[MinLengthValidator(3, "닉네임은 3자 이상이어야 합니다.")],
    )
    email = models.EmailField(
        blank=False,
        verbose_name="Email-address",
        max_length=100,
        unique=True,
        error_messages={"unique": "이미 사용중인 이메일입니다."},
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    profileImg = models.URLField(
        blank=True, 
        null=True, 
        default="https://api.cloudflare.com/client/v4/accounts/135e63e511ff302b43eaab2356b50bf6/images/v1/fccba4a0-df32-485d-8c6f-9410b97c2100"
    )

    age = models.PositiveIntegerField(
        blank=False,
        default=0,
        validators=[
            MinValueValidator(15, "15세 이상부터 가입이 가능합니다."),
        ],
    )
    phone = models.CharField(max_length=13, null=True, blank=True)

    is_admin = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=False)
    pick = models.ForeignKey(
        "idols.Idol",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )
    reports = models.ManyToManyField(
        "users.Report",
        null=True,
        blank=True,
        related_name="users",
    )
    selected_time = models.DateTimeField(default=datetime.now)#스케쥴 일자 
    
    def str(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Our_Users"


    # 회원 가입시 email 인증 로직 추가할 것.


# 제보
class Report(CommonModel):

    owner = models.ForeignKey(  
        "users.User",
        max_length=100,
        default="",
        on_delete=models.CASCADE,
        related_name="report",
    )
    ScheduleTitle = models.CharField(max_length=100, default="")
    ScheduleType = models.ForeignKey(
        "boards.Board",
        max_length=150,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="report",
    )
    location = models.CharField(max_length=100, default="")
    when = models.DateTimeField(default=datetime.now)#스케쥴 일자 
    whoes = models.ManyToManyField(  
        "idols.Idol",
        null=True,
        blank=True,
        related_name="report",
    )
    is_enroll=models.BooleanField(default=False)
    
    def str(self):
        return self.ScheduleTitle

    class Meta:
        verbose_name_plural = "User Report"
