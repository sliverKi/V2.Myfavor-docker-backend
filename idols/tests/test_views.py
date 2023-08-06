from django.urls import reverse
from rest_framework import status
from .test_models import IdolAPITestCase
from idols.models import Idol
from users.models import User
from boards.models import Board
from schedules.models import Schedule
from datetime import datetime
class IdolsGet(IdolAPITestCase):
    URL="/api/v2/idols/"
    def setUp(self):
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
    
    def test_get_list_idols_success(self):
        response=self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

class singleIdolPost(IdolAPITestCase):
    URL="/api/v2/idols/"
    help_text="idol 생성"
    
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


    def test_post_single_idol_sucess(self):
        self.client.login(email="admin@gmail.com", password="admin")  # 관리자로 로그인
        response = self.client.post(self.URL, self.idol_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Idol.objects.count(), 2)  # 새로운 아이돌이 추가되었는지 확인
        self.client.logout()
    
    def test_post_single_idol_fail_without_permission(self):
        self.client.login(email="test@gmail.com", password="test", is_admin=False)#관리자가 아닌 일반 사용자가 idol을 등록하는 경우
        response = self.client.post(self.URL, self.idol_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) #permissionDenied
        self.client.logout()

class IdolDetailTest(IdolAPITestCase):
    Base_URL="/api/v2/idols/"
    def test_get_single_idol(self):
        url=f"{self.Base_URL}{self.idol.idol_name_en}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["idol_name_en"], self.idol_data["idol_name_en"])

    def test_put_single_idol_sucess(self):
        url=f"{self.Base_URL}{self.idol.idol_name_en}/"
        #올바른 data
        self.client.login(email="admin@gmail.com", password="admin")#관리자 계정으로 로그인        
        valid_data={
            "idol_name_en":"UpdatedSunMi",
            "idol_birthday":"1993-05-02",
            }
        response_valid=self.client.put(url, valid_data, format="json")
        self.assertEqual(response_valid.status_code, status.HTTP_202_ACCEPTED)
        self.client.logout()
    
    def test_put_single_idol_fail_without_permission(self):    
        url=f"{self.Base_URL}{self.idol.idol_name_en}/"
        self.client.login(email="test@gmail.com", password="test", is_admin=False)#일반 사용자로 로그인
        valid_data={
            "idol_name_en":"UpdatedSunMi",
            "idol_birthday":"1992-12-01",
        }
        response_invalid=self.client.put(url, data=valid_data, format="json")
        self.assertEqual(response_invalid.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
    
    def test_put_single_idol_fail(self):    
        url=f"{self.Base_URL}{self.idol.idol_name_en}/"
        self.client.login(email="admin@gmail.com", password="admin", is_admin=False)#일반 사용자로 로그인    
        #올바르지 않은 data
        invalid_data_with_group={
            "idol_name_en":"",
            "group":["InValidGroup"],
            "idol_birthday":"1993-05-02",
        }
        response_with_group=self.client.put(url, invalid_data_with_group, format="json")
        self.assertEqual(response_with_group.status_code,status.HTTP_400_BAD_REQUEST )
        self.client.logout()

class ScheduleDateTest(IdolAPITestCase):
    Base_URL="/api/v2/idols/"
    
    
    def setUp(self):
        super().setUp() 
        self.cataegory_event=Board.objects.create(type=Board.BoardKinddChoices.EVENT)
        self.cataegory_broadcast=Board.objects.create(type=Board.BoardKinddChoices.BROADCAST)

        self.schedule1=Schedule.objects.create(
            ScheduleTitle="test-case schedule1",
            ScheduleType=self.cataegory_event,
            location="Korea",
            when="2023-09-01"
        )
        self.schedule1.participant.add(self.idol)

        self.schedule2=Schedule.objects.create(
            ScheduleTitle="test-case schedule2",
            ScheduleType=self.cataegory_broadcast,
            location="Seoul",
            when="2023-09-01"
        )
        self.schedule2.participant.add(self.idol)

    def test_get_all_schedules(self):
        url=f"{self.Base_URL}{self.idol.idol_name_en}/schedule/"
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_schedules_with_specific_categories(self):
        url=f"{self.Base_URL}{self.idol.idol_name_en}/schedule/"
        data = {
            "categories": ["broadcast", "release"],
            "when": "2023-08"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_schedules_with_no_categories(self):
        url=f"{self.Base_URL}{self.idol.idol_name_en}/schedule/"
        data = {
            "when": "2023-09"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_schedules_depth_day(self):
        url=f"{self.Base_URL}{self.idol.idol_name_en}/schedule/"
        invalid_data = {
            "when": "2023-09-01",
        }
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

    
class UpcomingSchedules(IdolAPITestCase):
    Base_URL="/api/v2/idols/"
    def setUp(self):
        pass

class TopIdols(IdolAPITestCase):
    URL="/api/v2/idols/rank/"
    def setUp(self):
        super().setUp() 
        idol_data_list = [
            {
                "idol_name_kr": "아이돌1",
                "idol_name_en": "Idol1",
                "idol_profile": "프로필1의 URL",
                "is_solo": True,
                "idol_birthday": "1990-01-01",
                "has_schedules": False,
                "pickCount": 10,
            },
            {
                "idol_name_kr": "아이돌2",
                "idol_name_en": "Idol2",
                "idol_profile": "프로필2의 URL",
                "is_solo": False,
                "idol_birthday": "1995-03-15",
                "has_schedules": True,
                "pickCount": 5,
            },
            {
                "idol_name_kr": "아이돌3",
                "idol_name_en": "Idol2",
                "idol_profile": "프로필2의 URL",
                "is_solo": False,
                "idol_birthday": "1995-03-15",
                "has_schedules": True,
                "pickCount": 9,
            },
            {
                "idol_name_kr": "아이돌4",
                "idol_name_en": "Idol2",
                "idol_profile": "프로필2의 URL",
                "is_solo": False,
                "idol_birthday": "1995-03-15",
                "has_schedules": True,
                "pickCount": 3,
            },
            {
                "idol_name_kr": "아이돌5",
                "idol_name_en": "Idol2",
                "idol_profile": "프로필2의 URL",
                "is_solo": False,
                "idol_birthday": "1995-03-15",
                "has_schedules": True,
                "pickCount": 15,
            }
        ]
        self.idols = [Idol.objects.create(**data) for data in idol_data_list]
    
    def test_get_idols_pickCount_rank(self):
        response=self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4) 
        prev_pick_count = response.data[0]["pickCount"]
        print("prev_pick_count", prev_pick_count)
        for idol_info in response.data[1:]:
            current_pick_count = idol_info["pickCount"]
            self.assertTrue(prev_pick_count >= current_pick_count)
            prev_pick_count = current_pick_count
        print("for loop: prev_pick_count", prev_pick_count)
        


