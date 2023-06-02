from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError, ValidationError
from .models import Groups
from idols.serializers import TinyIdolSerializer
from idols.models import Idol
from idols.serializers import IdolsListSerializer

class groupSerializer(ModelSerializer):

    class Meta:
        model=Groups
        fields=(
            "enter",
            "groupname",
            "group_profile"
        )


class groupDetailSerializer(ModelSerializer):
    member=TinyIdolSerializer(many=True, read_only=True)
    class Meta:
        model=Groups
        fields=(
            "enter",
            "groupname",
            "group_profile",
            "member", 
        )
    def create(self, validated_data):
        members_data=validated_data.pop("member",None)
        
        try:
            with transaction.atomic():#roll-back
                group=Groups.objects.create(**validated_data)
            if members_data:
                print(1)
                if isinstance(members_data, list):
                    print(2)
                    for member_data in members_data:
                        print(member_data)#유나(Yuna)
                
                        name=member_data.split("(")
                        print("name", name)
                        idol_name_kr=name[0].strip()
                        idol_name_en=name[1].replace(")","").strip()
                        idol, created= Idol.objects.get_or_create(
                            idol_name_kr=idol_name_kr, 
                            idol_name_en=idol_name_en,
                        )
                        print("idol, ",idol)
                        if created:
                            print(3)
                            group.member.add(idol)
                        else:
                            print(4)
                            group.member.add(idol.id)
                else:
                    member_data=get_object_or_404(Idol, idol_name_kr=members_data)
                    group.member.add(member_data)
            else:
                raise ParseError({"error":"잘못된 요청입니다."})  
     
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return group

            



"""
"create method input data"
{
    "enter": "SMTOWN",
    "groupname": "ASEPA",
    "member": ["윈터(Winter)", "카리나(Karina)", "지젤(Giselle)", "닝닝(Ning Ning)"],
    "group_profile": "https://i.namu.wiki/i/IDQUJdGfC8R290Ppttx1OxBiBeldm4_9mTZrwhEEbaHzsQ6Cai4RwO-nbcSBZwaBZQD187zUrVrc232UhkIcmx0DCyptVJRBiSqGQ-uvC9fk9rj8s0NQBLWZKkCZifGRnbXrDhAkzOocGXCmKcFTig.webp"
}
"""