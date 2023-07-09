from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Album
from groups.models import Group
import datetime
# from datetime import date
import requests
from PIL import Image
from io import BytesIO
import base64
import os
from django.conf import settings

class AlbumSerializer(ModelSerializer):
    class Meta:
        model=Album
        fields=("pk", "album_name", "album_cover")
    
class GroupAlbumSerializer(ModelSerializer):
    # groupname=serializers.CharField(source="group_artists.groupname", read_only=True)
    class Meta:
        model=Album
        fields=("pk","album_name", "release_date", "album_cover")
    
    def create(self, validated_data):
        group = self.context["group"]  #context에서 group 객체를 가져옴.
        album = Album.objects.create(group_artists=group,**validated_data)
        return album
    
    def update(self, instance, validated_data):
        album_name = validated_data.get("album_name", instance.album_name)
        album_cover = validated_data.get("album_cover", instance.album_cover)
        release_date = validated_data.get("release_date", instance.release_date)
        
        instance.album_name = album_name
        instance.album_cover = album_cover
        #img resize : 700*700
        if release_date is not None: 
            release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d").date()  # release_date 필드가 입력되었을 경우에만 처리
            if release_date > datetime.date.today():  # 오늘 날짜보다 미래인 경우
                raise serializers.ValidationError("Invalid release date.")
            instance.release_date = release_date
        
        instance.save()
        return instance
    
        
class SoloAlbumSerializer(ModelSerializer):
    class Meta:
        model =Album
        fields=("pk", "album_name","release_date", "album_cover")
    



"""
{
  "album_name": "Black Mamba - The 1st Single",
  "release_date": "2020-11-17",
  "album_cover": "https://a5.mzstatic.com/us/r1000/0/Music124/v4/1f/53/e2/1f53e291-df44-bb66-1c29-6e74c2b0eab0/aespa_BlackMamba_final.png"
} 

{
  "album_name": "Forever - The 2nd Single",
  "release_date": "2021-02-05",
  "album_cover": "https://a5.mzstatic.com/us/r1000/0/Music114/v4/e7/c0/e1/e7c0e1e1-8e51-2d16-56d1-f3e1e79ea144/aespa_Forever_DS.jpg"
} 

{
  "album_name": "NextLevel- The 3rd Single",
  "release_date": "2021-05-17",
  "album_cover": "https://a5.mzstatic.com/us/r1000/0/Music125/v4/60/8d/ac/608dacc2-d6d6-462d-26f0-d693e4364751/artwork.jpg"
} 
"""
"""update input data(group)
{  "album_name": "NextLevel- The 3rd Single"}
"""
