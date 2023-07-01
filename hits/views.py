from django.shortcuts import render
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from idols.models import Idol
from idols.serializers import IdolDetailSerializer, IdolsViewSerializer

class IdolsHits(APIView):
    def get(self, request):
        # Idol.objects.update(viewCount=F('viewCount') + 1)
        idols = Idol.objects.order_by('-viewCount')[:5]
        serializer = IdolsViewSerializer(idols, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class TopIdol(APIView):
    def get_object(self, idol_name_kr):
        try:
            return Idol.objects.get(idol_name_kr=idol_name_kr)
        except Idol.DoesNotExist:
            raise NotFound

    def get(self, request, idol_name_kr): 
        idol = self.get_object(idol_name_kr)
        idol.viewCount+=1
        idol.save()
        serializer = IdolDetailSerializer(
            idol,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)