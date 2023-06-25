from django.shortcuts import render
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Solo
from .serializers import soloSerializer
class SoloList(APIView):
    def get(self, request):
        all_solos=Solo.objects.all()
        serializer=soloSerializer(all_solos, many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
