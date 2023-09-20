from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from idols.models import Idol
from users.models import User

class IdolAPITestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@gmail.com", 
            password="admin",
            nickname="관리자",
            name="관리자",
            is_active=True,
            is_admin=True
        )
        self.user=User.objects.create(
            email="test@gmail.com",
            password="test",
            nickname="일반 사용자",
            name="일반 사용자",
            is_active=True,
            is_admin=False,
        )
        self.idol_data = {
            "idol_name_kr": "선미",
            "idol_name_en": "SunMi",
            "idol_profile": "https://image.kpopmap.com/2019/03/SunMi-063022.jpg",
            "is_solo": True,
            "idol_birthday": "1992-05-02",
            "has_schedules": False,
            "pickCount": 10,
        }
        self.idol = Idol.objects.create(**self.idol_data)

    def test_idol_creation(self):
        print("idol_name_en:", self.idol.idol_name_en)
        print("idol_name_kr:", self.idol.idol_name_kr)
        print("idol_profile:", self.idol.idol_profile)
        print("is_solo:", self.idol.is_solo)
        print("idol_birthday:", self.idol.idol_birthday)
        print("has_schedules:", self.idol.has_schedules)
        print("pickCount:", self.idol.pickCount)