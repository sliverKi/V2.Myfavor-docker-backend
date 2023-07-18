
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Idol
from boards.serializers import BoardSerializer
from schedules.models import Schedule


class slideName(ModelSerializer):
    idol=serializers.SerializerMethodField()
    class Meta:
        model=Idol
        fields=("idol",)
    def get_idol(self,obj):
        return f"{obj.idol_name_kr}({obj.idol_name_en})"
    

class soloSerializer(ModelSerializer):
    class Meta:
        model=Idol
        fields=("idol_name_kr","idol_name_en")
class TinyIdolSerializer(ModelSerializer):#groupDetail에서 사용
    class Meta:
        model=Idol
        fields=( "idol_name_kr","idol_name_en", "idol_profile", "idol_birthday")

class SimpleIdolInfoSerializer(ModelSerializer):#groupIdol에서 사용
    group=serializers.SerializerMethodField()
    class Meta:
        model=Idol
        fields=("group","has_schedules")
    def get_group(self, obj):
        return obj.group.values_list('groupname', flat=True)

class IdolsListSerializer(ModelSerializer):
    class Meta:
        model = Idol
        fields = (
            "pk", 
            "idol_name_kr",
            "idol_name_en", 
            "idol_profile",
            "idol_birthday", 
            "has_schedules"
        )



   

class IdolDetailSerializer(ModelSerializer):
    # fullname=serializers.SerializerMethodField()
    group=serializers.SerializerMethodField()
    # idol_schedules = ScheduleSerializer(many=True, read_only=True)  # 스케줄을 필수 항목으로 인식하지 않음
    class Meta:
        model = Idol
        fields = (
            "pk",
            "idol_name_kr",
            "idol_name_en",
            "idol_profile",
            "is_solo",
            "group",
            "idol_birthday",
            "has_schedules",
            )#viewCount,
            # "idol_schedules",
        
    # def get_fullname(self,obj):
    #     return f"{obj.idol_name_kr}({obj.idol_name_en})"
    
    def get_group(self, obj):
        return obj.group.values_list('groupname', flat=True)
    
    # def update(self, instance, validated_data):
    #     group_data=validated_data.pop("group", None)
    #     print(group_data)
    #     if group_data:
    #         instance.group.set(group_data)
    #     return instance

class PickIdolSerializer(ModelSerializer):#groupDetail에서 사용
    class Meta:
        model=Idol
        fields=( "idol_name_kr","idol_name_en", "idol_profile", "idol_birthday", "pickCount")