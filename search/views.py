from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from idols.models import Idol
from idols.serializers import TinyIdolSerializer

class SearchView(APIView):
#http://127.0.0.1:8000/api/v2/search/?q=winter
    def get(self, request):  
        search_query=request.GET.get('q')
    
        if not search_query and len(search_query)<2:
            return Response({"message: 검색 키워드를 2자 이상으로 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Idol.objects.filter(
            idol_name_kr__icontains=search_query
        ) | Idol.objects.filter(
            idol_name_en__icontains=search_query
        ) | Idol.objects.filter(
            group__groupname__icontains=search_query
        )
        #| Group.objects.filter(
           # groupname__icontains=search_query
        #)#error: Cannot combine queries on two different base models.~>장고 search filter 사용
        
        # icontains : 대소문자를 구분하지 않고 부분 일치하는 검색 수행
        if not queryset.exists():
            return Response({"message":"일치하는 검색 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TinyIdolSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
