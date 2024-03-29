from rest_framework.test import APITestCase
from solos.models import Solo  
from idols.models import Idol  
from users.models import User
import datetime
 

class SoloAPITestCase(APITestCase):
    
    def setUp(self):
        # Idol 인스턴스 생성
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
        self.idol = Idol.objects.create(
            idol_name_en="Jeon So Mi",
            idol_name_kr="전소미",
            idol_birthday="2001-03-09",
            idol_profile="https://image.kpopmap.com/2019/06/%EC%A0%84%EC%86%8C%EB%AF%B8.png",
            is_solo= True,
            has_schedules=False,
            pickCount=10
        )

        
        self.solo = Solo.objects.create(
            enter="THEBLACKLABEL",#
            solo_profile="https://image.kpopmap.com/2019/06/%EC%A0%84%EC%86%8C%EB%AF%B8.png",
            member=self.idol,
            solo_debut="2019-06-13",
            solo_insta="https://www.instagram.com/somsomi0309/?hl=ko",
            solo_youtube="https://www.youtube.com/channel/UCGrZ9Yu14T53h5YLsxOXkCw",
        )

    def test_solo_creation(self):
        self.assertIsInstance(self.solo, Solo)
        self.assertEqual(str(self.solo), f"{self.solo.member}")
    
