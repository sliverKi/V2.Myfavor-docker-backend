from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Board
from .serializers import BoardSerializer

class BoardType(APIView):
    def get(self, request):  # 일정 종류에 맞는 일정 조회
        all_boardType = Board.objects.all()
        serializer = BoardSerializer(all_boardType, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
