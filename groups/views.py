from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Group
from .serializers import groupSerializer, groupDetailSerializer
from idols.models import Idol
from idols.serializers import SimpleIdolInfoSerializer

class GroupList(APIView):#[OK]
    
    def get(self, request):
        all_groups = Group.objects.all()
        serializer = groupSerializer(all_groups, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):#관리자만이 아이돌 등록 가능 
        # if not request.user.is_admin:
        #     raise PermissionError
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
    
class GroupDetail(APIView):#[OK]
    def get_object(self, groupname):
        try:
            return Group.objects.get(groupname=groupname)
        except Group.DoesNotExist:
            raise NotFound
            
    def get(self, request, groupname):
        group=self.get_object(groupname)
        serializer=groupDetailSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, groupname):
        group=self.get_object(groupname)
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
        group=self.get_object(groupname)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class GroupIdol(APIView):
    def get_group(self, groupname):
        try:
            return Group.objects.get(groupname=groupname)
        except Group.DoesNotExist:
            raise NotFound
    
    def get_idol(self, group,idol_name_kr):
        try:
            return group.member.get(idol_name_kr=idol_name_kr)
        except Idol.DoesNotExist:
            raise NotFound
        
    def get(self, request, groupname, idol_name_kr):
        group=self.get_group(groupname)
        
        try:
            idol = self.get_idol(group, idol_name_kr)
            idol.viewCount+=1
            idol.save()
        except NotFound:
            return Response({"message": "Idol not found in the group."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SimpleIdolInfoSerializer(idol)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


        

