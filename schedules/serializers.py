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

        if ScheduleType_data:
            schedule_type = instance.ScheduleType
            new_type = ScheduleType_data.get('type')
            if new_type not in Category.objects.values_list('type', flat=True):
                raise ParseError("Invalid Category.")
            schedule_type.type = new_type
            schedule_type.content = ScheduleType_data.get('content', schedule_type.content)
            schedule_type.save()

        if participant_data:
            print("1", participant_data)
            for data in participant_data:
                idol, _ = Idol.objects.get_or_create(idol_name_kr=data["idol_name_kr"])
                instance.participant.add(idol)
        instance.save()
        return instance


"""
{
    "ScheduleType": {
        "type": "event",
        "content": "지젤 건강문제로 녹화 불참"
    }
}
or 
{
    "participant": [(수정 전 )
        {
            "idol_name_kr": "윈터",
            "idol_name_en": "Winter",
            "idol_profile": "https://newsimg.sedaily.com/2022/08/26/269Y4OKML1_1.jpg"
        }
    ]
}
{#수정 후 
    "participant": [{"닝닝"}]
}
or
{
    "ScheduleType": {
        "type": "broadcast",
        "content": "지젤 건강문제로 녹화 불참"
    },
    "participant": [
        {
            "idol_name_kr": "닝닝",
            "idol_name_en": "Ning Ning",
            "idol_profile": "https://newsimg.sedaily.com/2022/08/26/269Y4OKML1_1.jpg"
        }
    ]
}

"""