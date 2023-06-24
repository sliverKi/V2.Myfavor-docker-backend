from rest_framework.serializers import ModelSerializer
from idols.serializers import SimpleIdolInfoSerializer
from .models import IdolLike

class IdolLikeSerializer(ModelSerializer):
    class Meta:
        model= IdolLike
        fields=("idol",)