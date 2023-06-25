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
    member=TinyIdolSerializer(many=True, read_only=True)
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
                        for name, profile in member_data.items():
                            name=name.split("(")
                            
                            idol_name_kr = name[0]
                            idol_name_en = name[1].replace(")", "").strip()  # 이 부분은 필요에 따라 영어 이름을 설정할 수 있습니다
                            print(12)
                            idol, created = Idol.objects.get_or_create(
                                idol_name_kr=idol_name_kr,
                                idol_name_en=idol_name_en,
                                idol_profile=profile
                            )
                            group.member.add(idol)
                            idol.group.add(group)
                else:
                    print(2)
                    member_data=get_object_or_404(Idol, idol_name_kr=members_data)
                    group.member.add(member_data)
                    
            else:
                raise ParseError({"error":"잘못된 요청입니다."})  
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return group
    
    def update(self, instance, validated_data):#idol_birthday도 수정이 가능하게 할 것 
        # enter=validated_data.get("enter", None)
        # groupname=validated_data.get("groupname", None)
        # print(groupname)
        # print(enter)

        groupname=validated_data.pop("groupname", None)
        print("groupname: ", groupname)
        members_data=validated_data.pop("member", None)#멤버  리스트 
        print("members_data",members_data)
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
                        group=Group.objects.get(groupname=groupname)
                        if member not in group.member.all():
                            member.idol_profile=profile
                           
                            member.save()
                            group.member.add(member)
                            member.group.add(group)
                        print(member.idol_profile)

                    except Idol.DoesNotExist:
                        group=Group.objects.get(groupname=groupname)
                        new_member=Idol.objects.create(
                            idol_name_kr=idol_name_kr,
                            idol_name_en=idol_name_en,
                            idol_profile=profile
                        ) 
                        group.member.add(new_member)#추가가 안됌
                        new_member.group.add(group)
        return instance

"""
'update method input data'
기존에 있는 멤버 수정
{"member":[{"윈터(Winter)": 
"https://i.namu.wiki/i/QHpNxR1RkTxrjNou24zLPYBKuEdgG94_5tKijfVAZUqRUBY9yrR3dNNXStcNN3SDLTG3h1zj-V5edL1wNnLQVFlMvJzr0R2k6UHVnpuOyr4kNJEYNHeGmHN8DJsTlH_pEcz5O5VGyJr-61qyqLWuhQ.webp"}]}

새로운 멤버 추가
{"groupname":"ASEPA","member":[{"지젤(Giselle)":"https://i.namu.wiki/i/XZJ_uP4HrQAokcELQ5gTooP8R3l0yRE29GZpvnOyW8gQ8WXxuXhYyuhQcShptwOE-4WQQvzOzqDszOwCevFCsqgBC56NjCvyjadlIuFxy4t3RJNDDY0-BOLDDovejfMMTOzkxlmjt1iaMtBYlDBJxw.webp"}]}
{"groupname":"ITZY","member":[{"리아(Lia)":"https://i.namu.wiki/i/8uVrkEh4GN3I8_-pdVm99fU_pwWxTCVTj3tMNxg8nVBTCrlwM1SB_4h6HMeQF4-nCh7WLz6EiPfkSTC_Dv-9JHJnhc3o34_CbEVikiReKvRulKbMGirH48L2tJDtjWhcV_qnAK2znWhZJ3PX8xEHlw.webp"}]}

'create method input data'
 {
    "enter": "SMTOWN",
    "groupname": "ASEPA",
    "group_profile": "https://images8.alphacoders.com/118/1183043.jpg",
    "group_debut": "2020-11-17",
    "group_insta": "https://www.instagram.com/aespa_official/",
    "group_youtube": "https://www.youtube.com/channel/UC9GtSLeksfK4yuJ_g1lgQbg"
    "member": [
        {
            "카리나(Karina)":"https://i.namu.wiki/i/D8-LCYRc64tRedl74xk-IpVK2x7FyLnDUV8-ZRUgNdfi80miyGP0ItlcTJsjRJ_t81lvr2u1E8p6PW1LY2GyT8YEFOnTxw3sggQQ5zZ2U0DlgPPFlUsjHnDWn5W68wKlqcznasxRnw-OXIWP9LbYJw.webp"
        },
        {
            "윈터(Winter)":"https://i.namu.wiki/i/WAHQwL9akfInav0ir6owCGKMzX_9xCfrG615LM0qCYyzeFRXmLDl-_X-SPmGpirUCzgLPkKtKVaRQ45jRv97GqX_ZF-WwcXelqoTBHkGx_nF2sN50cPemD3XEwtLAwGInvsbMNt0O52l0qp_bIgbJw.webp"
        },
        {
            "지젤(Giselle)":"https://i.namu.wiki/i/bnB3M2qsxdKBrBJHZqohQ5JWZd2SUs0XIxh77FxlRyOaKKfkemB5VrCgmCKGXLHJSC0_XrDFtxitrY6nYrO_syKj93Ulvn06pHNRw3LG8s0Cjcm1hTFapxOoPj-LfLPE0cgtfDzjnAuKT146ZVfmQQ.webp"
        },
        {
            "닝닝(NingNing)":"https://i.namu.wiki/i/3jncwW5iYaKCVKZ1Dr1e0lwF-Z1LPlNI-ez9Telnwi0coltxCyFWfrTA_PZlhPgytySkzDoPO5VQBNWN2n6Vd6v5UsLF9-IjeV1AvV0CIdYiJoYM1uN1Obb82acAbe4RiqJ0JPLuT83CSuhihGefww.webp"
        }
    ]
} 
  {
    "enter": "JYP",
    "groupname": "ITZY",
    "group_profile": "https://i.namu.wiki/i/JWo3uUmDbgandQy4i0v_QoxuN5H-Th1dzI50ZumxXdlzO4UnHgtgbrF5jcKS1CwIpfeNuJANKWCv4xWO-KAlZABX4Coj0LY5hAd54zWaR5H7lJXhsxbgSp5AKCPLh2hrPKQigGiqElThmUI3BAIH2A.webp",
    "group_debut": "2019-02-12",
    "group_insta": "https://www.instagram.com/itzy.all.in.us/",
    "group_youtube": "https://www.youtube.com/channel/UCDhM2k2Cua-JdobAh5moMFg",
    "member": [
        {
            "예지(Yeji)":"https://i.namu.wiki/i/u8uIk39RuSRmvrZQOumzUqaN9XauBF0yohANELeX6BzAh27mDwPqP5GDyNXFWDxSm9UZTFteWOtE6USZ8pbG050k91nWHp7KyErhjWxjgPVtOz9ZyGOY-9rC-fFgiECfg1neUsza7WaXuLqZOaBG8A.webp"
        }
    ]
}
"""

