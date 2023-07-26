from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from .models import Schedule
from boards.models import Board
from boards.serializers import BoardSerializer
from idols.serializers import TinyIdolSerializer, soloSerializer
from idols.models import Idol
from idols.serializers import slideName

class slideScheduleSerializer(ModelSerializer):
    ScheduleType = BoardSerializer(read_only=True)
    participant=slideName(read_only=True, many=True)
    class Meta:
        model=Schedule
        fields=(
            "pk",
            "ScheduleTitle", 
            "ScheduleType", 
            "location", 
            "when", 
            "participant"
        )
        

class ScheduleSerializer(ModelSerializer):#admin user가 user's report 등록시 사용 
    owner=serializers.CharField(source='owner.nickname', read_only=True)
    ScheduleType = BoardSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = (
            "pk",
            "owner",
            "ScheduleTitle",
            "ScheduleType",
            "location",
            "when",
        )

class ScheduleDetailSerializer(ModelSerializer):
    ScheduleType = BoardSerializer(read_only=True)
    # participant = soloSerializer(many=True, read_only=True) #읽기 전용 필드 
    class Meta:
        model=Schedule
        fields=(
            "pk",
            "ScheduleTitle",
            "ScheduleType",
            "location",
            "when",
            "participant",
        )
    
    def create(self, validated_data):
        ScheduleType_data = validated_data.pop('ScheduleType', None)
        print("1", ScheduleType_data)
        participant_data = validated_data.pop('participant')
        try:
            with transaction.atomic():
                schedule=Schedule.objects.create(**validated_data)
                if ScheduleType_data:
                    print("2",ScheduleType_data)
                    ScheduleType=Board.objects.filter(type=ScheduleType_data).first()
                    schedule.ScheduleType=ScheduleType
                    schedule.save()
                if participant_data:
                    if isinstance(participant_data, list):
                        for participant in participant_data:
                            participant=get_object_or_404(Idol, idol_name_kr=participant)
                            schedule.participant.add(participant)
                            participant.has_schedules=True
                            participant.idol_schedules.add(schedule)
                            participant.save()
                    else:
                        participant=get_object_or_404(Idol, idol_name_kr=participant)
                        schedule.participant.add(participant)
                        participant.has_schedules=True
                        participant.idol_schedules.add(schedule)
                        participant.save()
                else:
                    raise ParseError({"error": "참여자를 알려주세요."})
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return schedule

    def update(self, instance, validated_data):
        ScheduleType_data=validated_data.pop("ScheduleType", instance.ScheduleType)
        print("1", ScheduleType_data)
        # participant_data=validated_data.pop("participant", instance.participant)
        ScheduleTitle=validated_data.pop("ScheduleTitle", instance.ScheduleTitle)
        location=validated_data.pop("location", instance.location)
        when=validated_data.pop("when", instance.when)

        instance.ScheduleTitle = ScheduleTitle
        instance.location = location
        instance.when = when

        instance.save()

        if ScheduleType_data:
            print("2", ScheduleType_data)
            for i in Board.objects.all():
                print(i.type)
            updated_type=Board.objects.filter(type=ScheduleType_data).first()
            instance.ScheduleType = updated_type
            instance.save()

        # if participant_data:
        #     instance.participant.clear()
        #     if isinstance(participant_data, list):
        #         for participant in participant_data:
        #             participant=get_object_or_404(Idol, idol_name_kr=participant)
        #             instance.participant.add(participant)
        #             participant.has_schedules=True
        #             participant.idol_schedules.add(instance)
        #             participant.save()
        #     else:
        #         participant=get_object_or_404(Idol, idol_name_kr=participant)
        #         instance.participant.add(participant)
        #         participant.has_schedules=True
        #         participant.idol_schedules.add(instance)
        #         participant.save()
        instance.save()
        return instance


"""
create-input data
{
    "ScheduleTitle": "음악방송 녹화",
    "ScheduleType": "broadcast",
    "location": "MBC",
    "when": "2023-07-17T15:30:00",
    "participant": ["사쿠라"]
}
"""

"""
update-input data
 {
"ScheduleTitle": "음악방송 녹화 : 인기가요", 
"location": "KBS광장", 
"when": "2023-07-18T16:30", 
"ScheduleType":"event", 
"participant":["닝닝", "사쿠라", "허윤진"](다수), ["닝닝"](한명 추가)
}
 

"""