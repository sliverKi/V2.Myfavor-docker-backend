import re
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework import serializers
from .models import User, Report
from idols.models import Idol
from idols.serializers import TinyIdolSerializer
from boards.serializers import BoardSerializer
from boards.models import Board
from django.db import transaction
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

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
  
    idol_name = serializers.SerializerMethodField(read_only=True)
    idol_profile = serializers.SerializerMethodField(source="pick.idol_profile", read_only=True)
    selected_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    
    def get_object(self, user):
        request = self.context["request"]
        return Idol.objects.filter(user=request.user, user__pk=user.pk).exists()
    
    class Meta:
        model = User
        fields = (
            "pk",
            "nickname",
            "email",
            "phone",
            "profileImg",
            "pick",
            "idol_name",
            "idol_profile",
            "selected_time",
            "is_admin",
            
        )
        extra_kwargs = {
            'nickname': {'read_only': True},
        }

    def get_idol_name(self, user):
        pick=user.pick
        if pick:
            return f"{pick.idol_name_kr} ({pick.idol_name_en})"
        return None
     
    def get_idol_profile(self, user):
        pick=user.pick
        return pick.idol_profile if pick else None
    
    def validate_pick(self, value):
        # 사용자가 최소 1일(필요에 따라 timedelta를 조정하세요) 이상 "pick"을 변경한 경우만 업데이트를 허용합니다.
        selected_time = self.instance.selected_time
        if selected_time:
            # min_update_day = 1
            min_update_time = selected_time + timedelta(minutes=2) #timedelta(days=min_update_day)
            if timezone.now() < min_update_time:
                raise ValidationError("최소 2분이 지나야 'pick'을 업데이트할 수 있습니다.")
        return value

    def update(self, instance, validated_data):
        # "pick"을 업데이트하기 전에 "last_pick_change_time"을 최신으로 갱신합니다.
        instance.selected_time = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    

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
            # "password"
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
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


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
        owner_nickname = validated_data.pop('owner')
        print("3", owner_nickname)
        ScheduleType_data = validated_data.pop('ScheduleType', None)
        print("1", ScheduleType_data)
        try:
            with transaction.atomic():
                owner = User.objects.get(nickname=owner_nickname)
                whoes_data = [owner.pick]
                print("4-1", whoes_data)
                print("4", owner)
                report=Report.objects.create(owner=owner, **validated_data)
                report.whoes.set(whoes_data)
                if ScheduleType_data:
                    print("2",ScheduleType_data)
                    ScheduleType=Board.objects.filter(type=ScheduleType_data).first()
                    report.ScheduleType=ScheduleType
                    report.save()
                return report
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

          
    
    def update(self, instance, validated_data):
        ScheduleType_data=validated_data.pop("ScheduleType", instance.ScheduleType)
        ScheduleTitle=validated_data.pop("ScheduleTitle", instance.ScheduleTitle)
        location=validated_data.pop("location", instance.location)
        print("1",location)
        when=validated_data.pop("when", instance.when)
        whoes=validated_data.pop("whoes", instance.whoes)
        print("2", whoes)
        
        instance.ScheduleTitle = ScheduleTitle
        instance.location = location
        instance.when = when
        
        instance.save()

        if ScheduleType_data:
            print("3", ScheduleType_data)
            for i in Board.objects.all():
                print(i.type)
            updated_type=Board.objects.filter(type=ScheduleType_data).first()
            instance.ScheduleType = updated_type
            instance.save()
        if whoes:
            instance.whoes.clear()
            if not whoes:
                raise ParseError("제보할 아이돌을 알려 주세요.")
            if len(set(whoes)) != 1:
                raise ParseError("한명의 아이돌에 대해서만 등록이 가능합니다.")
            idol_name = whoes[0].split("(")[0].strip()
               
            try:
                idol = Idol.objects.get(Q(idol_name_kr=idol_name) | Q(idol_name_en=idol_name))
                instance.whoes.add(idol)

            except Idol.DoesNotExist:
                raise ParseError("선택하신 아이돌이 없어요.")
        return instance




"""
user-report create-data
{
    "ScheduleType": "broadcast",
    "ScheduleTitle": "post test create function",
    "location": "USA",
    "when": "2023-07-25T15:34:03+09:00"
}

update-data

{   "ScheduleTitle": "post test in July",
    "ScheduleType": "event",
    "location": "Incheon",
    "when": "2023-07-26T15:30:00"
}

{
    "ScheduleTitle": "post test in July",
    "ScheduleType": "event",
    "location": "Incheon",
    "when": "2023-07-26T15:30:00",
    "whoes": ["지수(Jisu)"]#관리자가 보고대상에대해 수정할때 
}
"""
    
    
        

