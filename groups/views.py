from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Group
from .serializers import groupSerializer, groupDetailSerializer
from idols.models import Idol
from idols.serializers import TinyIdolSerializer, SimpleIdolInfoSerializer

class getGroup:
    def get_group(self, groupname):
        try:
            return Group.objects.prefetch_related('member').get(groupname=groupname).order_by("pk")
        except Group.DoesNotExist:
            raise NotFound

class GroupList(APIView):#[OK]
    
    def get(self, request):
        all_groups = Group.objects.prefetch_related().order_by("pk")
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
                group_debut=request.data.get("group_debut"),
                group_insta=request.data.get("group_insta"),
                group_youtube=request.data.get("group_youtube"),
            )
            serializer=groupDetailSerializer(
                group, context={'request':request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupDetail(getGroup, APIView):#[OK]
            
    def get(self, request, groupname):
        group=self.get_group(groupname)
        serializer=groupDetailSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, groupname):
        group=self.get_group(groupname)
        if not request.user.is_admin:
            raise PermissionError
        print(group)
        serializer=groupDetailSerializer(
            group,
            data=request.data,
            partial=True
        )
        print(request.data)
        if serializer.is_valid():
            updated_group=serializer.save(   
            groupname=request.data.get("groupname"),
            member=request.data.get("member"), 
            )
            return Response(groupDetailSerializer(updated_group).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, groupname):
        group=self.get_group(groupname)
        if not request.user.is_admin:
            raise PermissionError
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class GroupIdol(getGroup, APIView):
    
    def get_idol(self, group,idol_name_en):
        try:
            return group.member.get(idol_name_en=idol_name_en)
        except Idol.DoesNotExist:
            raise NotFound
        
    def get(self, request, groupname, idol_name_en):
        group=self.get_group(groupname)
        try:
            idol = self.get_idol(group, idol_name_en)
        except NotFound:
            return Response({"message": "Idol not found in the group."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TinyIdolSerializer(idol)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, group, idol_name_en):
        idol=self.get_idol(group, idol_name_en)
        if not request.user.is_admin: 
            raise PermissionDenied
        idol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

