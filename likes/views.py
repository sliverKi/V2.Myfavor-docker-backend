from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from idols.models import Idol
class IdolLike(APIView):
    def post(self, request,idol_name_kr):
        pass