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
        fake=Faker()
        
        count = options['count']
        
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)

        if count<=0:
            self.stdout.write(self.style.WARNING("Please provide a positive count value."))
            return 
        seeder=Seed.seeder()
        seeder.add_entity(Schedule, count, {
            'ScheduleTitle': lambda x: fake.sentence(),
            'ScheduleType': lambda x: Board.objects.order_by('?').first(),
            'location': lambda x: fake.address(),
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