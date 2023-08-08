from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Board
from .serializers import BoardSerializer
from django.core.cache import cache
import logging
from config.settings import DEBUG

if not DEBUG:#개발서버 베포인 경우
    class BoardType(APIView):
        def get(self, request):  # 일정 종류에 맞는 일정 조회
            all_boardType = Board.objects.all()
            serializer = BoardSerializer(all_boardType, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

else:#개발환경인 경우
    class BoardType(APIView):
        def get(self, request):  # 일정 종류에 맞는 일정 조회
            cache_key = "board_cache"

            # Try to get data from cache
            cached_data = cache.get(cache_key)
            if cached_data:
                logger = logging.getLogger(__name__)
                logger.info(f"Cache HIT for key: {cache_key}")
                return Response(cached_data, status=status.HTTP_200_OK)

            # If cache miss, query data from the database
            all_boardType = Board.objects.all()
            serializer = BoardSerializer(all_boardType, many=True)

            # Save data to cache
            cache.set(cache_key, serializer.data, 60 * 30)  # Cache for 30 minutes
            #1day=>86400(60*60*24) 
            return Response(serializer.data, status=status.HTTP_200_OK)


