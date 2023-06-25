
from rest_framework.serializers import ModelSerializer
from .models import Solo

class soloSerializer(ModelSerializer):

    class Meta:
        model=Solo
        fields=("enter", "solo_profile", "member")
