from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from albums.models import Album
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
        # print("group",group)
        
        serializer = GroupAlbumSerializer(
            data=request.data,
            context={'group':group}
        )
        # print("re", request.data)
        if serializer.is_valid():
            album=serializer.save()
            serializer=GroupAlbumSerializer(
                album, context={'request':request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupAlbumDetail(APIView):
    def get_groupname(self, groupname):
        try:
            return Group.objects.get(groupname=groupname)
        except Group.DoesNotExist:
            raise NotFound
    
    def get_album(self, groupname, pk):
        try:
            return Album.objects.get(group_artists=groupname, pk=pk)
        except Album.DoesNotExist:
            raise NotFound
        
    def get(self, request, groupname, pk):
        group=self.get_groupname(groupname)
        try:
            album = self.get_album(group, pk)
        except NotFound:
            return Response({"message": "Album not found in the group."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupAlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,groupname, pk):
        group=self.get_groupname(groupname)
        album=self.get_album(group, pk)
        
        if not request.user.is_admin:
            raise PermissionError
 
        serializer = GroupAlbumSerializer(
            album,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            updated_album=serializer.save(
                # album_name=request.data.get("album_name"),
                release_date=request.data.get("release_date"),
                # album_cover=request.data.get("album_cover")
            )
            serializer=GroupAlbumSerializer(updated_album)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, groupname, pk):
        album = self.get_album(groupname, pk)
        if not request.user.is_admin: 
            raise PermissionDenied
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

        


class SoloAlbum(APIView):
    def get(self, request):
        pass
