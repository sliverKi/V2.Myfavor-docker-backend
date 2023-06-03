from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError, ValidationError
from .models import Groups
from idols.serializers import TinyIdolSerializer
from idols.models import Idol
from idols.serializers import IdolsListSerializer

class groupSerializer(ModelSerializer):#groupList

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
                        for name, profile in member_data.items():
                            print("3",name)
                            name=name.split("(")
                            print(name)
                            idol_name_kr = name[0]
                            idol_name_en = name[1].replace(")", "").strip()  # 이 부분은 필요에 따라 영어 이름을 설정할 수 있습니다
                            
                            idol, created = Idol.objects.get_or_create(
                                idol_name_kr=idol_name_kr,
                                idol_name_en=idol_name_en,
                                idol_profile=profile
                            )
                            group.member.add(idol)
                else:
                    member_data=get_object_or_404(Idol, idol_name_kr=members_data)
                    group.member.add(member_data)
            else:
                raise ParseError({"error":"잘못된 요청입니다."})  
     
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return group
    def update(self, instance, validated_data):
        pass
"""
"create method input data"
 {
    "enter": "SMTOWN",
    "groupname": "ASEPA",
    "group_profile": "https://i.namu.wiki/i/IDQUJdGfC8R290Ppttx1OxBiBeldm4_9mTZrwhEEbaHzsQ6Cai4RwO-nbcSBZwaBZQD187zUrVrc232UhkIcmx0DCyptVJRBiSqGQ-uvC9fk9rj8s0NQBLWZKkCZifGRnbXrDhAkzOocGXCmKcFTig.webp",
    "member": [
        {
            "윈터(Winter)":"https://talkimg.imbc.com/TVianUpload/tvian/TViews/image/2022/10/08/1fe0c521-2351-49ed-98c9-ffb6e9d6d53b.jpg"
        },
        {
            "닝닝(Ning Ning)":"https://talkimg.imbc.com/TVianUpload/tvian/TViews/image/2022/10/08/1fe0c521-2351-49ed-98c9-ffb6e9d6d53b.jpg"
        }
    ]
} 
"""