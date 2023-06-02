from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Groups
from .serializers import groupSerializer

# Create your views here.
class GroupList(APIView):
    
    def get(self, request):
        all_groups = Groups.objects.all()
        serializer = groupSerializer(all_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):#관리자만이 아이돌 등록 가능 
        if not request.user.is_admin:
            raise PermissionError
        serializer=groupSerializer(data=request.data)
        if serializer.is_valid():
            group=serializer.save(
                member=request.data.get("member")
            )
            serializer=groupSerializer(
                group, context={'request':request}
            )
            return Response(groupSerializer(group).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


        

