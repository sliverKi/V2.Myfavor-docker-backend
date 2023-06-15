from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import requests
from .models import Photo
from rest_framework import status 

import boto3
from uuid import uuid4
from datetime import datetime
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
    AWS_S3_CUSTOM_DOMAIN

)

class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
   
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if request.user.is_admin:
            photo.delete()
        return Response(status=status.HTTP_200_OK)    

        
class GetUploadURL(APIView):
    def post(self, request):
        url= f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(url, headers={
            "Authorization":f"Bearer {settings.CF_TOKEN}"
        })
        one_time_url = one_time_url.json()
        result=one_time_url.get('result')
        return Response({"id":result.get("id"), "uploadURL": result.get('uploadURL')})
    

# class GetS3URL(APIView): #[공지]aws credit 받을수 있다고 하심-> 버킷, iam 삭제함 크레딧 받은 후에 연결할 것 
#     def post(self, request):
#         file=request.data.get('filename')
#         user=request.user
#         if file:
#             uuid_name=uuid4.hex
#             image_datetime=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             fileobj_key=uuid_name+" "+image_datetime
#             # file_extension=file.name.split('.')[-1]

#             s3_client=boto3.client(
#                 "s3",
#                 aws_access_key_id=AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#             )

#             s3_client.upload_fileobj(
#                 file,
#                 AWS_STORAGE_BUCKET_NAME,
#                 fileobj_key,
#                 ExtraArgs={
#                     "ContentType": file.content_type,
#                 },
#             )
#             image_url=AWS_S3_CUSTOM_DOMAIN+fileobj_key
#             user.profileImg=image_url
#             user.save()

#             return Response({"image_url": image_url}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"error":"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            

