import random 
from django.core.management.base import BaseCommand
from faker import Faker
from django_seed import Seed
from schedules.models import Schedule
from boards.models import Board
from idols.models import Idol
from datetime import datetime
class Command(BaseCommand):
    help="generate random Schedule data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            default=0,
            type=int,
            help="how many schedules data, do you want to create?"
        )
    
    def handle(self, *args, **options):
        fake=Faker("ko-KR")
        
        count = options['count']
        
        start_date = datetime(2023, 7, 1)
        end_date = datetime(2023, 12, 31)

        if count<=0:
            self.stdout.write(self.style.WARNING("Please provide a positive count value."))
            return 
        seeder=Seed.seeder()
        seeder.add_entity(Schedule, count, {
            'ScheduleTitle': lambda x: fake.sentence(),
            'ScheduleType': lambda x: Board.objects.order_by('?').first(),
            'location': lambda x: fake.random_element(elements=['CK아트홀','예문아트홀', '국립극장 별오름극장', '케이아트 디딤홀', 
                                                                '홍익대 대학로 아트센터', 'COEX 아트홀', '대구 콘서트 하우스 체임버홀', 
                                                                '예스24 스테이지', '예술의 전당 음악당 리싸이클 홀', 'LG아트센터 서울 U+ 스테이지', 
                                                                '부산시민회관 소극장', '링크아트센터 벅스홀', '연세대학교 아트홀', 
                                                                '백암아트홀', '게릴라', '월드컵 경기장', '한국예술종합학교 예술극장', 
                                                                '세종문화회관', '두산아트센터 연강홀', '이화여자대학교 삼성홀', 'COEX 아티움', 
                                                                'TheK 아트홀', '수원SK아트리움 대극장', 'Melon Music Award', '가온 K차트홀', 
                                                                '지니 뮤직스테이지', '상암MBC', 'KBS광장',]),
            'when': lambda x: fake.date_time_between(start_date=start_date, end_date=end_date),
        })
        inserted_pks = seeder.execute()
        schedules = Schedule.objects.filter(pk__in=inserted_pks[Schedule])
        

        for schedule in schedules:
            idols = Idol.objects.order_by('?')[:fake.random_int(min=1, max=3)]
            schedule.participant.set(idols)
            for idol in idols:
                idol.idol_schedules.add(schedule)
                idol.has_schedules=True
                idol.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} schedules."))