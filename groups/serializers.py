from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError, ValidationError
from .models import Group
from idols.serializers import TinyIdolSerializer
from idols.models import Idol
from idols.serializers import IdolsListSerializer

class groupSerializer(ModelSerializer):#groupList

    class Meta:
        model=Group
        fields=(
            "pk",
            "groupname",
            "group_profile",
            "group_debut",
            "group_insta",
            "group_youtube",
        )


class groupDetailSerializer(ModelSerializer):
    member=TinyIdolSerializer(many=True,read_only=True)
    class Meta:
        model=Group
        fields=(
            "pk",
            "enter",
            "groupname",
            "group_profile",
            "group_debut",
            "group_insta",
            "group_youtube",
            "member", 
        )
    def create(self, validated_data):#아이돌 생일도 받을것 
        members_data=validated_data.pop("member",None)
        try:
            with transaction.atomic():#roll-back
                group=Group.objects.create(**validated_data)
            if members_data:
                if isinstance(members_data, list):
                    for member_data in members_data:
                        for name, info in member_data.items():
                            name=name.split("(")
                            idol_name_kr = name[0]
                            idol_name_en = name[1].replace(")", "").strip()  # 이 부분은 필요에 따라 영어 이름을 설정할 수 있습니다
                            profile=info.get("profile")
                            idol_birthday=info.get("idol_birthday")
                            print(12)
                            idol, created = Idol.objects.get_or_create(
                                idol_name_kr=idol_name_kr,
                                idol_name_en=idol_name_en,
                                idol_profile=profile,
                                idol_birthday=idol_birthday,
                            )
                            group.member.add(idol)
                            idol.group.add(group)
                else:
                    print(2)
                    name, info = members_data.items()[0]
                    name = name.split("(")
                    idol_name_kr = name[0]
                    idol_name_en = name[1].replace(")", "").strip()
                    profile = info.get("profile")
                    idol_birthday = info.get("idol_birthday")
                    member_data = get_object_or_404(
                        Idol, 
                        idol_name_kr=idol_name_kr,
                        idol_name_en=idol_name_en,
                        idol_profile=profile,
                        idol_birthday=idol_birthday,
                    )
                    group.member.add(member_data)
            else:
                raise ParseError({"error":"잘못된 요청입니다."})  
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return group
    
    def update(self, instance, validated_data):#idol_birthday도 수정이 가능하게 할 것 
        groupname=validated_data.pop("groupname", None)
        members_data=validated_data.pop("member", None)#멤버  리스트 
        enter = validated_data.pop("enter", instance.enter)
        group_insta=validated_data.pop("group_insta", instance.group_insta)
        group_youtube=validated_data.pop("group_youtube", instance.group_youtube)
        
        instance.enter = enter
        instance.group_insta = group_insta
        instance.group_youtube = group_youtube

        instance.save()

        print("members:", members_data)
        if members_data:    
            for name, info in members_data.items():   
                name=name.split("(")
                idol_name_kr=name[0].strip()                    
                idol_name_en=name[1].replace(")", "").strip()
                profile=info.get("profile")
                idol_birthday=info.get("idol_birthday")
                try:
                    print(1)
                    member=Idol.objects.get(idol_name_kr=idol_name_kr)
                    group=Group.objects.get(groupname=groupname)
                    if member not in group.member.all():
                        member.idol_profile=profile
                        member.idol_birthday=idol_birthday
                        member.save()
                        group.member.add(member)
                        member.group.add(group)
                    # print(member.idol_profile)
                    else:
                        member.idol_profile=profile
                        member.idol_birthday=idol_birthday
                        member.save()

                except Idol.DoesNotExist:
                    print(2)
                    group=Group.objects.get(groupname=groupname)
                    new_member=Idol.objects.create(
                        idol_name_kr=idol_name_kr,
                        idol_name_en=idol_name_en,
                        idol_profile=profile,
                        idol_birthday=idol_birthday
                    ) 
                    group.member.add(new_member)
                    new_member.group.add(group)
        return instance

"""
'update method input data'
( 그룹에 새로운 멤버 추가 또는 기존의 멤버 수정 )
{
    "groupname": "BLACKPINK",(필수)
    "member": {
        "리사(Lisa)": {
            "profile": "https://i.namu.wiki/i/iOatgawg2prYRPY8xJPV5H7rwv2aFJWKWCyNTJOu314mQIVWTBCiHiCC_0Tsa60CkJpmV7giNS2KGEpnnR1dibh8eGflBdp4Vg-CnHoDf720giCGK4GjLgzsP4jqFvGM6HSOPcbz7mqlKx4IBpG5EA.webp",
            "idol_birthday": "1997-03-27"
        }
    }
}

'create method input data'
{
    "enter": "YG",
    "groupname": "BLACKPINK",
    "group_profile": "https://image.kpopmap.com/2019/03/BLACKPINK-082322.jpg",
    "group_debut": "2016-08-08",
    "group_insta": "https://www.instagram.com/blackpinkofficial/",
    "group_youtube": "https://www.youtube.com/@BLACKPINK",
    "member": [
        {
            "지수(Jisu)": {
                "profile": "https://image.kpopmap.com/2019/03/jisoo_profile_s_0215.jpg",
                "idol_birthday": "1995-01-03"
            }
        },
        {
            "로제(Rose)": {
                "profile": "https://image.kpopmap.com/2019/03/BLACKPINK-Rose-082322.jpg",
                "idol_birthday": "1997-02-11"
            }
        },
        {
            "제니(Jenny)": {
                "profile": "https://image.kpopmap.com/2019/03/BLACKPINK-Jennie-082322.jpg",
                "idol_birthday": "1996-01-16"
            }
        },
        {
            "리사(Lisa)": {
                "profile": "https://image.kpopmap.com/2019/03/BLACKPINK-Lisa-082322.jpg",
                "idol_birthday": "1997-03-27"
            }
        }
    ]
}
"""

