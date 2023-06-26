from django.shortcuts import render
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Solo
from .serializers import soloSerializer
class SoloList(APIView):
    def get(self, request):
        all_solos=Solo.objects.all()
        serializer=soloSerializer(all_solos, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=soloSerializer(data=request.data)
        print("re",request.data)
        if serializer.is_valid():
            solo=serializer.save(
                enter=request.data.get("enter"),
                solo_profile=request.data.get("solo_profile"),
                member=request.data.get("member"),
                idol_birthday=request.data.get("idol_birthday")
            )
            serializer=soloSerializer(
                solo, context={"request":request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoloDetail(APIView):
    def get_object(self, idol_name_kr):
        try:
            return Solo.objects.get(idol_name_kr=idol_name_kr)
        
        except Solo.DoesNotExist:
            raise NotFound
    # def get(self, request, idol_name_kr):
    #     solo=self.get_object(idol_name_kr)
    #     serializer=