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
            return Solo.objects.get(member__idol_name_kr=idol_name_kr)
        except Solo.DoesNotExist:
            raise NotFound
        
    def get(self, request, idol_name_kr):
        solo=self.get_object(idol_name_kr)
        idol=solo.member
        # print("idol", idol)
        idol.viewCount+=1
        # print(idol.viewCount)
        idol.save()
        serializer=soloSerializer(
            solo,
            context={"request": request},
        )
        response_data = serializer.data#response_data 딕셔너리에 "viewCount" 필드를 추가, 
        response_data["viewCount"] = idol.viewCount #해당 필드의 값을 Idol 모델의 viewCount 값으로 설정
        return Response(response_data, status=status.HTTP_200_OK)#Solo 모델의 정보와 viewCount 값을 함께 반환
    
    