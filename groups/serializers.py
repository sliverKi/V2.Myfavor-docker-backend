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
    member=TinyIdolSerializer(many=True, read_only=True)
    class Meta:
        model=Groups
        fields=(
            "belong",
            "Girl_group",
            "Boy_group",
            "member",
            "group_profile",
            
        )
        read_only_fields=("is_solo",)
    def create(self, validated_data):
        members_data=validated_data.pop("member",None)

        print("members_data: ", members_data)
        # print(boys)
        
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
                        idol_name_kr=name[0].strip()
                        idol_name_en=name[1].replace(")","").strip()
                        idol, created= Idol.objects.get_or_create(
                            idol_name_kr=idol_name_kr, 
                            idol_name_en=idol_name_en
                        )
                        
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
    "belong": "JYP",
    "Girl_group": "ITZY",
    "Boy_group": null,
    "member": ["예지(Yeji)", "유나(Yuna)", "류진(Ryujin)", "채령(Chaeryeong)", "리아(Lia)"],
    "group_profile": "https://i.namu.wiki/i/KfffiUF2eqAwiloVp_lFRtnxrkHnoh1HwKywtJ0MM6bOncyetGT4qZyIWItH2rX-WcUOqM_kmQuKU2tfYXJiKg.webp"
}
"""