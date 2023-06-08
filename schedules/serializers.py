from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import Schedule
from categories.models import Category
from categories.serializers import CategorySerializer
from idols.serializers import TinyIdolSerializer
from idols.models import Idol

class ScheduleSerializer(ModelSerializer):

    ScheduleType = CategorySerializer(read_only=True)
    participant = TinyIdolSerializer(many=True, read_only=True) #읽기 전용 필드 
    when=serializers.DateTimeField()

    class Meta:
        model = Schedule
        fields = (
            "pk",
            "ScheduleTitle",
            "ScheduleType",
            "location",
            "when",
            "participant",
        )

    def update(self, instance, validated_data):
        ScheduleType_data=validated_data.pop("ScheduleType", None)
        participant_data=validated_data.pop("participant", None)
        print(1)
        print(Category.objects.all())
        if ScheduleType_data:

            schedule_type = instance.ScheduleType
            new_type = ScheduleType_data.get('type')
            if new_type not in Category.objects.values_list('type', flat=True):
                raise ParseError("Invalid Category.")
            schedule_type.type = new_type
            schedule_type.content = ScheduleType_data.get('content', schedule_type.content)
            # for attr, value in ScheduleType_data.items():
                # print("attrs: ", attr)#type, content
                # setattr(schedule_type, attr, value)#schedule_type이라는 객체에, attr이라는 이름의 속성에 value 값을 할당
            schedule_type.save()

        if participant_data:
            # instance.participant.clear()
            for data in participant_data:
                idol, _ = Idol.objects.get_or_create(idol_name_kr=data["idol_name_kr"])
                instance.participant.add(idol)

        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        instance.save()
        return instance


"""
{
    "ScheduleType": {
        "type": "event",
        "content": "지젤 건강문제로 녹화 불참"
    }
}
"""