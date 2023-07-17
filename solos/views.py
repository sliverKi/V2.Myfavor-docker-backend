from django.shortcuts import render
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from .models import Solo
from .serializers import soloSeiralizer, soloDetailSerializer
class SoloList(APIView):
    def get(self, request):
        all_solos=Solo.objects.all().order_by("pk")
        serializer=soloSeiralizer(all_solos, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_admin:
            raise PermissionError
        serializer=soloDetailSerializer(data=request.data)
        print("re",request.data)
        if serializer.is_valid():
            solo=serializer.save(
                enter=request.data.get("enter"),
                solo_profile=request.data.get("solo_profile"),
                member=request.data.get("member"),
                idol_birthday=request.data.get("idol_birthday"),
                solo_debut=request.data.get("solo_debut"),
                solo_insta=request.data.get("solo_insta"),
                solo_youtube=request.data.get("solo_youtube"),
            )
            serializer=soloDetailSerializer(
                solo, context={"request":request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoloDetail(APIView):
    def get_object(self, idol_name_en):
        try:
            return Solo.objects.get(member__idol_name_en=idol_name_en)
        except Solo.DoesNotExist:
            raise NotFound
        
    def get(self, request, idol_name_en):
        solo=self.get_object(idol_name_en)
        idol=solo.member
        
        serializer=soloDetailSerializer(
            solo,
            context={"request": request},
        )
        response_data = serializer.data #response_data 딕셔너리에 "viewCount" 필드를 추가, 
        
        return Response(response_data, status=status.HTTP_200_OK)#Solo 모델의 정보와 viewCount 값을 함께 반환
    
    def put(self, request, idol_name_en):#수정이 안됌
        solo=self.get_object(idol_name_en)
        if not request.user.is_admin:
            raise PermissionError
        serializer=soloDetailSerializer(
            solo,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            updated_solo=serializer.save()
            return Response(soloDetailSerializer(updated_solo).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, idol_name_en):
        solo=self.get_object(idol_name_en)
        if not request.user.is_admin: 
            raise PermissionDenied
        solo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)