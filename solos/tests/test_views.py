from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .test_models import SoloAPITestCase
from solos.models import Solo
from idols.models import Idol  

class SoloListTests(SoloAPITestCase):
    URL = '/api/v2/solos/'
    def setUp(self):
        super().setUp()
        

    def test_get_all_solos(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # def test_post_solo_not_admin(self):
    #     response = self.client.post(self.URL, {
    #         "enter": "New Enter",
    #         "solo_profile": "http://newprofile.com",
    #         "member": self.idol.id,
    #         "solo_insta": "http://newinsta.com",
    #         "solo_youtube": "http://newyoutube.com",
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # 여기서는 PermissionError가 403으로 반환됩니다.

    # def test_post_solo_as_admin(self):
    #     self.client.login(email="admin@gmail.com", password="admin")
        
    #     response = self.client.post(self.URL, {
    #         "enter": "New Enter",
    #         "solo_profile": "http://newprofile.com",
    #         "member": self.idol.id,
    #         "solo_insta": "http://newinsta.com",
    #         "solo_youtube": "http://newyoutube.com",
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
