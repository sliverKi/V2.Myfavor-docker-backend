from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import Idol, Schedule
from categories.serializers import CategorySerializer
from rest_framework.status import HTTP_400_BAD_REQUEST


class TinyIdolSerializer(ModelSerializer):#groupList에서 사용
    class Meta:
        model=Idol
        fields=( "idol_name_kr","idol_name_en", "idol_profile")



class IdolsListSerializer(ModelSerializer):
    class Meta:
        model = Idol
        fields = (
            "pk", 
            "idol_name_kr",
            "idol_name_en", 
            "idol_profile",
            "idol_debut",
            "idol_anniv", 
            "idol_birthday", 
            "idol_gender",
            "has_scheduels"
            )


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

class DateScheduleSerializer(ModelSerializer):
    ScheduleType = CategorySerializer(read_only=True)

    year=serializers.SerializerMethodField()
    month=serializers.SerializerMethodField()
    day=serializers.SerializerMethodField()
    class Meta:
        model=Schedule
        fields=(
            "pk",
            "ScheduleTitle", 
            "ScheduleType", 
            "location", 
            #"when", 
            "year", 
            "month", 
            "day"
        )
    def get_year(self, obj):
        return obj.when.year
    def get_month(self, obj):
        return obj.when.month
    def get_day(self, obj):
        return obj.when.day




class IdolDetailSerializer(ModelSerializer):
    
    idol_schedules = ScheduleSerializer(many=True, read_only=True)  # 스케줄을 필수 항목으로 인식하지 않음
    

    class Meta:
        model = Idol
        fields = "__all__"
    
    def validate(self, attrs):
        idol_name_kr=attrs.get('idol_name_kr')
        idol_name_en=attrs.get('idol_name_en')

        idol_gender=attrs.get('idol_gender')
        idol_solo=attrs.get('idol_solo')
        Girl_group=attrs.get('Girl_group')
        Boy_group=attrs.get('Boy_group')

        if idol_name_kr and not idol_name_en:
            raise ParseError("영문 이름을 입력해 주세요.")
        if not idol_name_kr and idol_name_en:
            raise ParseError("국문 이름을 입력해 주세요.")
            

        if idol_gender=="Man":
            if idol_solo=="GirlSolo" or Boy_group=="GirlGroup":
                raise ParseError("남자인 아이돌은 여성 항목을 선택할 수 없습니다.")
        else:
            if idol_solo=="BoySolo" or Girl_group=="BoyGroup":
                raise ParseError("여자인 아이돌은 남성 항목을 선택할 수 없습니다.")
            

        return attrs    