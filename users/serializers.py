import re
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework import serializers
from .models import User, Report
from idols.models import Idol
from idols.serializers import TinyIdolSerializer
from boards.serializers import BoardSerializer
from boards.models import Board
from django.db import transaction

# class HtmlSerializer(serializers.Serializer):
#     html_field = serializers.CharField()


# pick 수정~> 유효시간 설정하기 
class PickSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pick",)
    
    def update(self, instance, validated_data):
        current_pick = instance.pick
        print("cur", current_pick)
        new_pick = validated_data.get("pick")
        print("new", new_pick)
        # 새로운 "pick"과 기존 "pick"이 다를 경우에만 처리
        if current_pick and current_pick != new_pick:
            # 기존에 "pick"한 아이돌의 pickCount를 -1로 감소시킴
            current_pick.pickCount -= 1
            current_pick.save()
            # 새로운 아이돌로 업데이트하고 pickCount를 +1로 증가시킴
            instance.pick = new_pick
            instance.save()
            if new_pick:
                new_pick.pickCount += 1
                new_pick.save()
        return instance


# 캘린더에서 사용할 유저 정보
class CalendarSerializer(serializers.ModelSerializer):
    pick = TinyIdolSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
      
            "nickname",
            "pick",
        )

# 가장 적은 유저 정보(유저 스케줄에 나타낼 정보)
class SimpleUserSerializers(serializers.ModelSerializer):
   
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "nickname",
            "email",
            "pick",
            "is_admin",
        )

    def get_is_admin(self, user):
        request = self.context["request"]
        return user.is_admin == request.user.is_admin


# admin 조회 용
class TinyUserSerializers(serializers.ModelSerializer):
  
    def get_object(self, user):
        request = self.context["request"]
        return Idol.objects.filter(user=request.user, user__pk=user.pk).exists()

    class Meta:
        model = User
        fields = (
            "pk",
            "nickname",
            "email",
            "pick",
            "phone",
            "is_admin",
            "profileImg",
        )


# 회원가입 시 사용하는 정보
class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "nickname",
            "pick",
            "email",
            "phone",
            "age",
        )

    def validate_age(self, age):
        print("check age")
        if age:
            if age <= 14 and age >= 0:
                raise ParseError("15세 부터 가입 가능합니다.")
        else:
            raise ParseError("나이를 입력해 주세요.")
        return age

    def validate_password(self, password):
        if password:
            if not re.search(r"[a-z]", password):
                raise ValidationError("비밀번호는 영문 소문자를 포함해야 합니다.")
            if not re.search(r"[A-Z]", password):
                raise ValidationError("비밀번호는 영문 대문자를 포함해야 합니다.")
            if not re.search(r"[0-9]", password):
                raise ValidationError("비밀번호는 숫자를 포함해야 합니다.")
            if not re.search(r'[~!@#$%^&*()_+{}":;\']', password):
                raise ValidationError("비밀번호는 특수문자(~!@#$%^&*()_+{}\":;')를 포함해야 합니다.")
            if len(password) < 8 or len(password) > 16:
                raise ValidationError("비밀번호는 8자 이상 16자 이하이어야 합니다.")
            print(password)
        else:
            raise ParseError("비밀번호를 입력하세요.")
        return password
    
    def validated_phone(self, phone):
        phone = re.compile(r"^010\d{4}\d{4}$")
        data = data.replace("-", "")
        if not phone.match(data):
            raise serializers.ValidationError("유효한 형식을 입력하세요.")
        return data


# admin이 유저 정보를 조회할 때 사용하는 정보
class UserSerializer(serializers.ModelSerializer):

    pick = TinyIdolSerializer(read_only=True)
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "nickname",
            "age",
            "email",
            "pick",
            "is_admin",
        )

    def get_is_admin(self, user):
        request = self.context["request"]
        return user.is_admin == request.user.is_admin


class ReportSerializer(serializers.ModelSerializer):
    ScheduleType = BoardSerializer(read_only=True)

    class Meta:
        model=Report
        fields=("pk", "ScheduleTitle", "ScheduleType", "when", "is_enroll")


class ReportDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.nickname', read_only=True)
    whoes = serializers.SerializerMethodField()
    ScheduleType = BoardSerializer(read_only=True)

    class Meta:
        model = Report
        fields = (
            "pk",
            "owner",
            "ScheduleTitle",
            "ScheduleType",
            "location",
            "when",
            "whoes",
            "is_enroll"
        )
    
    def get_whoes(self, instance):
        whoes = instance.whoes.all()
        return [
            f"{idol.idol_name_kr}({idol.idol_name_en})"
            for idol in whoes
        ]
 
    def create(self, validated_data):
        ScheduleType_data = validated_data.pop('ScheduleType', None)
        print("1", ScheduleType_data)
        try:
            with transaction.atomic():
                report=Report.objects.create(**validated_data)
                if ScheduleType_data:
                    print("2",ScheduleType_data)
                    ScheduleType=Board.objects.filter(type=ScheduleType_data).first()
                    report.ScheduleType=ScheduleType
                    report.save()
                
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return report



