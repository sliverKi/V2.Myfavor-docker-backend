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
                if isinstance(members_data, list):
                    for member_data in members_data:
                        for name, profile in member_data.items():
                            name=name.split("(")
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
        # enter=validated_data.get("enter", None)
        # groupname=validated_data.get("groupname", None)
        # print(groupname)
        # print(enter)

        groupname=validated_data.pop("groupname", None)
        print("groupname: ", groupname)
        members_data=validated_data.pop("member", None)#멤버  리스트 
        # print("members_data",members_data)
        if members_data:
            for member_data in members_data:
                print("member_data", member_data)
                for name, profile in member_data.items():
                    print("name", name)
                    print("profile", profile)
                    name=name.split("(")
                    idol_name_kr=name[0].strip()
                    print("kr-name", idol_name_kr)
                    idol_name_en=name[1].replace(")", "").strip()
                    print("en-name", idol_name_en)
                    try:
                        member=Idol.objects.get(idol_name_kr=idol_name_kr)
                        member.idol_profile=profile
                        member.save()
                        #error: "str' object has no attribute 'save'
                        print(member.idol_profile)

                    except Idol.DoesNotExist:
                        group=Groups.objects.get(groupname=groupname)
                        new_member=Idol.objects.create(
                            idol_name_kr=idol_name_kr,
                            idol_name_en=idol_name_en,
                            idol_profile=profile,
                        ) 
                        group.member.add(new_member)#추가가 안됌
                        

        return instance

"""
'update method input data'
기존에 있는 멤버 수정
{"member":[{"윈터(Winter)": 
"https://i.namu.wiki/i/QHpNxR1RkTxrjNou24zLPYBKuEdgG94_5tKijfVAZUqRUBY9yrR3dNNXStcNN3SDLTG3h1zj-V5edL1wNnLQVFlMvJzr0R2k6UHVnpuOyr4kNJEYNHeGmHN8DJsTlH_pEcz5O5VGyJr-61qyqLWuhQ.webp"}]}

새로운 멤버 추가
{"groupname":"ASEPA","member":[{"지젤(Giselle)":"https://i.namu.wiki/i/XZJ_uP4HrQAokcELQ5gTooP8R3l0yRE29GZpvnOyW8gQ8WXxuXhYyuhQcShptwOE-4WQQvzOzqDszOwCevFCsqgBC56NjCvyjadlIuFxy4t3RJNDDY0-BOLDDovejfMMTOzkxlmjt1iaMtBYlDBJxw.webp"}]}

'create method input data'
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


{"enter":"SmTOWN", "groupname":"asepa","member":[{"윈터(Winter)": 
"https://i.namu.wiki/i/5WmvTTY-p-I_6KjWkmGtrl7ZEpyu2bnHXAo4ZQSXO5N1DCwXQPPTwBQXryg7cfbJDvwV6AskBG1W0uBVh-LSoX5qIMff7jh1OmFkmoN6qbXi38IJwq53uiZ5cSl3erR-hs2cmfRC2mdlc-6d909QEA.webp"}]}

"""