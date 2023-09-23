from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from idols.models import Idol
from users.models import User
from groups.models import Group 

class GroupAPITestCase(APITestCase):
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
        self.idol1 = {
            "idol_name_kr": "윈터",
            "idol_name_en": "Winter",
            "idol_profile": "https://image.kpopmap.com/2020/10/%ED%94%84%EB%A1%9C%ED%95%84-%EC%9C%88%ED%84%B0.png",
            "is_solo": False,
            "idol_birthday": "2001-01-01",
            "has_schedules": False,
            "pickCount": 10,
        }
        self.idol2 = {
            "idol_name_kr": "카리나",
            "idol_name_en": "Karina",
            "idol_profile": "https://image.kpopmap.com/2020/10/%ED%94%84%EB%A1%9C%ED%95%84-%EC%B9%B4%EB%A6%AC%EB%82%98.png",
            "is_solo": False,
            "idol_birthday": "2000-04-11",
            "has_schedules": False,
            "pickCount": 10,
        }
        self.idol1 = Idol.objects.create(**self.idol1)
        self.idol2 = Idol.objects.create(**self.idol2)
        
        self.group = Group.objects.create(
            enter= "SM",
            groupname= "AESPA",
            group_profile= "https://image.kpopmap.com/2020/10/%ED%94%84%EB%A1%9C%ED%95%84-%EC%97%90%EC%8A%A4%ED%8C%8C.png",
            group_debut= "2020-11-17",
            group_insta= "https://www.instagram.com/aespa_official/",
            group_youtube= "https://www.youtube.com/channel/UC9GtSLeksfK4yuJ_g1lgQbg"
        )
        self.group.member.add(self.idol1, self.idol2)
    
    def test_group_creation(self):
        self.assertIsInstance(self.group, Group)
        self.assertEqual(str(self.group), "AESPA")
    
    def test_count_group_member(self):
        self.assertEqual(self.group.member.count(), 2)



