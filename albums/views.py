from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from groups.models import Group
from .serializers import GroupAlbumSerializer

class GroupAlbum(APIView):
    def get_object(self, groupname):
        try: 
            return Group.objects.get(groupname=groupname)
        except Group.DoesNotExist:
            raise NotFound
    
    def get(self, request,groupname):
        group=self.get_object(groupname)
        albums=group.albums_group.all().order_by("release_date")
        serializer=GroupAlbumSerializer(albums, many=True)
        data={
            "groupname":group.groupname,
            "albums":serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, groupname):
        if not request.user.is_admin:
            raise PermissionError
        group=self.get_object(groupname=groupname)
        print("group",group)
        
        serializer = GroupAlbumSerializer(
            data=request.data,
            context={'group':group}
        )
        print("re", request.data)
        if serializer.is_valid():
            album=serializer.save()
            serializer=GroupAlbumSerializer(
                album, context={'request':request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SoloAlbum(APIView):
    def get(self, request):
        pass
