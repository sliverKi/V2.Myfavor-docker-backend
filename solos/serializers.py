from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.serializers import ModelSerializer
from .models import Solo

from idols.models import Idol
from idols.serializers import TinyIdolSerializer
from idols.models import Idol

class soloSerializer(ModelSerializer):
    # member=soloSerializer(read_only=True)
    idol_name_kr=serializers.CharField(source="member.idol_name_kr", read_only=True)
    idol_name_en=serializers.CharField(source="member.idol_name_en", read_only=True)
    idol_birthday=serializers.DateField(source="member.idol_birthday", write_only=True)
    
    class Meta:
        model=Solo
        fields=("pk", "solo_profile", "idol_name_kr", "idol_name_en", "idol_birthday", "enter")
    
    def create(self, validated_data):
        solo_profile=validated_data.get("solo_profile", None)
        members_data=validated_data.get("member", None)
        idol_birthday = validated_data.get("idol_birthday", None)
        try:
            with transaction.atomic():
                solo=Solo.objects.create(
                    enter=validated_data.get("enter"),
                    solo_profile=solo_profile
                    
                )
            if members_data:
                member_name = members_data.split("(")[0]
                idol = Idol.objects.filter(idol_name_kr=member_name).first()
                
                if not idol:
                    idol_name_en = members_data.split("(")[1].replace(")", "").strip()
                    idol = Idol.objects.create(
                        idol_name_kr=member_name,
                        idol_name_en=idol_name_en,
                        idol_profile=solo_profile,
                        idol_birthday=idol_birthday,
                    )
                solo.member = idol
                solo.save()
                idol.is_solo = True
                idol.save() 
            else:
                raise ParseError({"error": "잘못된 정보 요청입니다."})
        except Exception as e:
            raise ValidationError({"error": str(e)})
        return solo

"""create data
{
  "enter": "Stone Music",
  "solo_profile": "https://i.namu.wiki/i/ldJsKue_OFYnlarjBkqQdHosNGXgmUzknp_48jvO7f9sWSBpWJ7l4uIWcRF4Oquhn5DKEnmd0Zhvi3nNUIVLTwAKj8kSKJlmFx-4JVwzIN4mzn7Zj-w3paaNKQMUd21uxZN5igva8RrjAdumiOKjgw.webp",
  "member": "청하(ChungHa)",
  "idol_birthday":"2016-05-04"
}
"""







       




#solo_profile, idol_anme_kr, idol_name_en, 
#detail: idol_prifile