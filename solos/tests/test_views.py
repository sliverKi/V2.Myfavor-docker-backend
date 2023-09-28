from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .test_models import SoloAPITestCase
from solos.models import Solo
from idols.models import Idol  
import json
class SoloListTests(SoloAPITestCase):
    URL = '/api/v2/solos/'
    def setUp(self):
        super().setUp()
        self.idol=Idol.objects.create(
            idol_name_kr="권은비",
            idol_name_en= "Jang Wong Younga",
            idol_profile= "https://image.kpopmap.com/2019/01/KwonEunBi_profile_s_0601.jpg",
            idol_birthday= "1995-09-27",
            has_schedules=False,
            is_solo= True,
            pickCount= 10
        )
        

    def test_get_all_solos(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_solo_not_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.URL, {
            "enter": "Woolim",
            "solo_profile": "https://image.kpopmap.com/2019/01/KwonEunBi_profile_s_0601.jpg",
            "member": self.idol.id,
            "solo_insta": "http://newinsta.com",
            "solo_youtube": "http://newyoutube.com",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # 여기서는 PermissionError가 403으로 반환됩니다.
        self.client.logout()

    def test_post_solo_as_admin(self):
        self.client.login(email="admin@gmail.com", password="admin")
        member_name = f"{self.idol.idol_name_en}({self.idol.idol_name_kr})"
        response = self.client.post(self.URL, 
            {
                "enter": "Stone Music",
                "solo_profile": "https://i.namu.wiki/i/ldJsKue_OFYnlarjBkqQdHosNGXgmUzknp_48jvO7f9sWSBpWJ7l4uIWcRF4Oquhn5DKEnmd0Zhvi3nNUIVLTwAKj8kSKJlmFx-4JVwzIN4mzn7Zj-w3paaNKQMUd21uxZN5igva8RrjAdumiOKjgw.webp",
                "member": member_name,
                "idol_birthday":"2016-05-04",
                "solo_debut":"2017-06-07",
                "solo_youtube":"https://www.youtube.com/channel/UC9Gxb0gMCh3EPIDLQXeQUog",
                "solo_insta":"https://www.instagram.com/CHUNGHA_official"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class SoloDetailTests(SoloAPITestCase):
    Base_URL = '/api/v2/solos/'
    def setUp(self):
        super().setUp()
   
    
    def test_get_solo_detail(self):
        url = f"{self.Base_URL}{self.solo.member.idol_name_en}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['idol_name_en'], self.solo.member.idol_name_en)
    
    def test_update_solo_detail(self):
        url = f"{self.Base_URL}{self.solo.member.idol_name_en}/"
        self.client.login(email="admin@gmail.com", password="admin")
        new_data={
            "idol_name_en":"jeon somi",
            "idol_name_kr":"라리사노반", 
            "enter":"YG Family"
        }
        response = self.client.put(url, data=new_data, format='json')
        print("test", response.data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        updated_solo = Solo.objects.get(pk=self.solo.pk)
        self.assertEqual(updated_solo.member.idol_name_en, new_data['idol_name_en'])
        self.client.logout()
        

       

