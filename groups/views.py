from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Groups
from .serializers import groupSerializer, groupDetailSerializer

# Create your views here.
class GroupList(APIView):
    
    def get(self, request):
        all_groups = Groups.objects.all()
        serializer = groupSerializer(all_groups, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):#관리자만이 아이돌 등록 가능 
        if not request.user.is_admin:
            raise PermissionError
        serializer=groupDetailSerializer(data=request.data)
        print("re: ", request.data)
        if serializer.is_valid():
            group=serializer.save(
                enter=request.data.get("enter"),
                groupname=request.data.get("groupname"),
                member=request.data.get("member"),
            )
            serializer=groupDetailSerializer(
                group, context={'request':request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupDetail(APIView):
    def get_object(self, groupname):
        try:
            return Groups.objects.get(groupname=groupname)
        except Groups.DoesNotExist:
            raise NotFound
            
    def get(self, request, groupname):
        group=self.get_object(groupname)
        serializer=groupDetailSerializer(group)
        return Response(serializer.data)
    
    def put(self, request, groupname):#idol_profile 수정 할 수 있게 할 것, 
        group=self.get_object(groupname)
        serializer=groupDetailSerializer(
            group,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            updated_group=serializer.save()
            return Response(groupDetailSerializer(updated_group).data, status=status.HTTP_202_ACCEPTED)
        
    def delete(self, request, groupname):
        group=self.get_object(groupname).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    



        

