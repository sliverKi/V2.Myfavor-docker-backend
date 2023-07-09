from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from albums.models import Album
from groups.models import Group
from solos.models import Solo
from .serializers import AlbumSerializer, GroupAlbumSerializer, SoloAlbumSerializer

class GroupAlbum(APIView):
    def get_object(self, groupname):
        try: 
            return Group.objects.get(groupname=groupname)
        except Group.DoesNotExist:
            raise NotFound
    
    def get(self, request,groupname):
        group=self.get_object(groupname)
        albums=group.albums_group.all().order_by("release_date")
        serializer=AlbumSerializer(albums, many=True)
        data={
            "artists":group.groupname,
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
    def get_object(self, idol_name_kr):
        try:
            return Solo.objects.get(member__idol_name_kr=idol_name_kr)
        except Solo.DoesNotExist:
            raise NotFound
        
    def get(self, request, idol_name_kr):
        solo=self.get_object(idol_name_kr)
        print("1",solo)
        albums=solo.albums_solo.all().order_by("release_date")
        serializer=AlbumSerializer(albums, many=True)
        data={
            "artists":solo.member.idol_name_kr,
            "albums":serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, idol_name_kr):
        if not request.user.is_admin:
            raise PermissionDenied
        solo = self.get_object(idol_name_kr)
        serializer = SoloAlbumSerializer(
            data=request.data,
            context={'solo': solo}
        )
        if serializer.is_valid():
            album = serializer.save(solo_artists=solo)
            serialized_album = SoloAlbumSerializer(album, context={'request': request})
            return Response(serialized_album.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SoloAlbumDetail(APIView):
    
    def get_solo(self, idol_name_kr):
        try:
            return Solo.objects.get(member__idol_name_kr=idol_name_kr)
        except Solo.DoesNotExist:
            raise NotFound
    
    def get_album(self, solo, pk):
        try:
            return Album.objects.get(solo_artists=solo, pk=pk)
        except Album.DoesNotExist:
            raise NotFound
    
    def get(self, request, idol_name_kr, pk):
        solo = self.get_solo(idol_name_kr)
        album = self.get_album(solo, pk)
        serializer = SoloAlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self, request,idol_name_kr, pk):
        solo=self.get_solo(idol_name_kr)
        album=self.get_album(solo, pk)
        
        if not request.user.is_admin:
            raise PermissionError
 
        serializer = SoloAlbumSerializer(
            album,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_album=serializer.save(
                # album_name=request.data.get("album_name"),
                release_date=request.data.get("release_date"),
                # album_cover=request.data.get("album_cover")
            )
            serializer=SoloAlbumSerializer(updated_album)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, idol_name_kr, pk):
        solo=self.get_solo(idol_name_kr)
        album = self.get_album(solo, pk)
        if not request.user.is_admin: 
            raise PermissionDenied
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    """
    {
  "album_name": "No.1 - 2nd Album",
  "release_date": "2002-04-12",
  "album_cover": "https://a5.mzstatic.com/us/r1000/0/Music5/v4/65/e8/71/65e8711b-dc79-e1c6-1f35-9d2176b22c71/BoA_No1.jpg"
} 

{

    "album_name": "에잇 - 6th Digital Single",
    "release_date": "2020-05-06",
    "album_cover": "https://a5.mzstatic.com/us/r1000/0/Music125/v4/6b/65/4d/6b654d71-ed85-c6c4-8fe2-ef3d8e9f2ee0/cover_-.jpg"
}
    """