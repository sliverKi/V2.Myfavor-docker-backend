from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from idols.models import Idol
from idols.serializers import TinyIdolSerializer

class SearchView(APIView):

    def get(self, request):  
        search_query=request.GET.get('q')
        
        if not search_query and len(search_query)<2:
            raise ValidationError("message: 검색 키워드를 2자 이상으로 입력해 주세요.")
        
        if search_query not in Idol.objects.all():
            raise NotFound
        
        queryset = Idol.objects.filter(
            idol_name_kr__icontains=search_query
        ) | Idol.objects.filter(
            idol_name_en__icontains=search_query
        )

        # 필요한 직렬화기를 사용하여 검색 결과를 직렬화합니다.
        serializer = TinyIdolSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    