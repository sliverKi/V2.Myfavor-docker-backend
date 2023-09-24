from rest_framework import status
from idols.models import Idol
from groups.models import Group 
from users.models import User
from .test_models import GroupAPITestCase
from rest_framework.exceptions import NotFound, PermissionDenied
import json
class GroupGet(GroupAPITestCase):
    URL="/api/v2/groups/"
    def setUp(self):
        super().setUp()#test_models.py에 정의된 setUp상속
        
        self.idol=Idol.objects.create(
            idol_name_kr="장원영",
            idol_name_en= "Jang Wong Younga",
            idol_profile= "https://image.kpopmap.com/2019/01/IVE-WonYoung-082322.jpg",
            idol_birthday= "2004-08-31",
            has_schedules=False,
            pickCount= 10,
        )
        
        self.group = Group.objects.create(
            enter= "StarShip",
            groupname= "IVE",
            group_profile= "https://image.kpopmap.com/2021/11/IVE-082322.jpg",
            group_debut= "2021-12-22",
            group_insta= "https://www.instagram.com/ivestarship/",
            group_youtube= "https://www.youtube.com/@IVEstarship"
        )
        self.group.member.add(self.idol)
   
    def test_get_group_exists(self):
        response = self.client.get(self.URL)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group_names= [group['groupname'] for group in response.data] 
        self.assertIn("IVE", group_names)
        for group in response.data:
            if group['groupname']=='IVE':
                self.assertEqual(self.group.member.count(), 1)

    def test_get_group_does_not_exist(self):
        response = self.client.get(f"{self.URL}/9999/")  # 존재하지 않는 ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GroupPost(GroupAPITestCase):
    URL="/api/v2/groups/"
    def setUp(self):      
        super().setUp()

    
    def test_create_new_group_as_admin(self):
        self.client.login(email="admin@gmail.com", password="admin")
        data={
            "enter":"JYP",
            "groupname":"ITZY",
            "group_profile": "https://image.kpopmap.com/2019/01/itzy-profile.png",
            "group_debut": "2019-02-12",
            "group_insta": "https://www.instagram.com/itzy.all.in.us/?hl=ko",
            "group_youtube": "https://www.youtube.com/channel/UCDhM2k2Cua-JdobAh5moMFg",
            "member": [
                {
                "카리나(Karina)": {
                    "idol_profile": self.idol2.idol_profile,
                    "idol_birthday": self.idol2.idol_birthday,
                    }
                }
            ]
        }
        response=self.client.post(self.URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['groupname'], 'ITZY')
        self.client.logout
    
    def test_create_new_group_as_non_admin(self):       
        self.client.force_authenticate(user=self.user)  # 관리자 계정으로 인증
        
        data={
            "enter":"JYP",
            "groupname":"ITZY",
            "group_profile": "https://image.kpopmap.com/2019/01/itzy-profile.png",
            "group_debut": "2019-02-12",
            "group_insta": "https://www.instagram.com/itzy.all.in.us/?hl=ko",
            "group_youtube": "https://www.youtube.com/channel/UCDhM2k2Cua-JdobAh5moMFg",
            "member": [
                {
                "윈터(Winter)": {
                    "idol_profile": self.idol2.idol_profile,
                    "idol_birthday": self.idol2.idol_birthday,
                    }
                }
            ]
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

