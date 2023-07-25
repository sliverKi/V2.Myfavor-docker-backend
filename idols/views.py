from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,PermissionDenied,ParseError
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_202_ACCEPTED, 
    HTTP_204_NO_CONTENT, 
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN, 
    HTTP_404_NOT_FOUND 
)
from rest_framework.filters import SearchFilter

from .models import Idol
from .serializers import  TinyIdolSerializer, IdolsListSerializer, IdolDetailSerializer, PickIdolSerializer
from boards.models import Board
from boards.serializers import BoardSerializer
from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule
from medias.serializers import PhotoSerializer
from groups.models import Group
from datetime import datetime
from django.utils.dateformat import DateFormat


class getIdol:
    def get_idol(self, idol_name_en): 
        try:
            return Idol.objects.get(idol_name_en=idol_name_en)
        except Idol.DoesNotExist:
            raise NotFound
        
class Idols(APIView): #[수정OK]
    
    def get(self, request):

        all_idols = Idol.objects.prefetch_related().order_by("pk")
        serializer = IdolsListSerializer(all_idols, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):  
        
        if not request.user.is_admin: 
            raise PermissionDenied
        serializer = IdolDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            idol = serializer.save()
            return Response(IdolsListSerializer(idol).data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    """
    post input data
        {
            "idol_name_kr":"카리나",
            "idol_name_en":"Karina",
            "idol_profile":"https://i.namu.wiki/i/OsLvNXbYOYIMIe8ttpDZn1jLL0JL3RFZmZcmAWXMvcg7hYvHtX8Np4njdPC5SVlugrL6fjRyLZd_Prk-h9BB2v13y-dtP7eQKaKkcWTXNq21M6m2D0rpYLTfW1NsYhVXFB5fyOF4XdqMtU4UWwxCiQ.webp",
            "idol_birthday":"2000-04-11",
            "idol_debut":"2020-11-17"
        }
    """



class IdolDetail(getIdol, APIView): #[수정OK]

    # def get_object(self, idol_name_en): 
    #     try:
    #         return Idol.objects.get(idol_name_en=idol_name_en)
    #     except Idol.DoesNotExist:
    #         raise NotFound

    def get(self, request, idol_name_en): 
        idol = self.get_idol(idol_name_en)
       
        serializer = IdolDetailSerializer(
            idol,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, idol_name_en): 
        if not request.user.is_admin:
            raise PermissionDenied

        idol=self.get_idol(idol_name_en)
        if request.user.is_admin:
            serializer=IdolDetailSerializer(
                idol,  # user-data
                data=request.data,
                partial=True,
            )
            # print("re : ", request.data)
        if serializer.is_valid():
            groups=request.data.get("group")
            # print("group: ", groups)
            idol_schedules=request.data.get("idol_schedules")
            if groups:
                if not isinstance(groups, list):
                    raise ParseError("Invalid group")
                for group in groups:
                    # print(group)
                    # print(groups)
                    try:
                        group=Group.objects.get(groupname=group)
                    except Group.DoesNotExist:
                        raise ParseError({"message": "그룹을 먼저 생성해 주세요."})
                    idol.group.add(group)
                    group.member.add(idol)
                    
            if idol_schedules:
                if not isinstance(idol_schedules, list):
                    raise ParseError("Invalid schedules")
                idol.idol_schedules.clear()
                for idol_schedule_pk in idol_schedules: 
                    try:
                        schedule = Idol.objects.get(pk=idol_schedule_pk)
                        idol.idol_schedules.add(schedule)
                    except Schedule.DoesNotExist:
                        raise ParseError("Schedule not Found")
            updated_idol_schedules = serializer.save()
            return Response(IdolDetailSerializer(updated_idol_schedules).data, status=HTTP_202_ACCEPTED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        """
        put input data
        {
            "group":["ASEPA"],
            "idol_name_en":"Winter",
            "idol_birthday":"2001-01-01", 
            "idol_profile":"https://i.namu.wiki/i/j1mSQz1rUEGD8yslNgSdyWgHTaMeVMP0T6z45HuNUoKXSg3XZ92sQOeWKRI4bUEwCyy0YaI-tPrGEEhEIZlrSrZM4WA2qy0TvYL_TC6X6x79QowHTp8h6ECieB24d3TybWT5VZvF7X66cf86yI48gg.webp"
        }
        """

    def delete(self, request, idol_name_en): 
        idol=self.get_idol(idol_name_en)
       
        if request.user.is_admin==False: 
            raise PermissionDenied
        idol.delete()
        if idol.DoesNotExist:
            return Response(status=HTTP_204_NO_CONTENT)    

class IdolSchedule(getIdol, APIView): #수정[pagenation]:10개 적용할 것

    # def get_object(self, idol_name_en):

    #     try:
    #         return Idol.objects.get(idol_name_en=idol_name_en)
    #     except Idol.DoesNotExist:
    #         raise NotFound

    def get(self, request, idol_name_en):

        idol = self.get_idol(idol_name_en)
        serializer = ScheduleSerializer(
            
            idol.idol_schedules.all(),
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)

    
    def post(self, request, idol_name_en):#관리자가 아이돌 스케쥴을 등록하려는 경우 사용되어짐. 
        #아이돌 스케줄이 등록되면 hasSchedule을 false에서 true로 변경 할 것 (participant 에 있는 아이들도 같이 바꿀것 )
        idol=self.get_idol(idol_name_en)
        serializer=ScheduleSerializer(data=request.data)
        
        if not request.user.is_admin:
            raise PermissionDenied
        
        else:
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                schedule = serializer.save()
        # 1. ScheduleType 에 있는 필드가 Category에 없는 경우, 유저가 입력한 내용을 새롭게 db에 생성(ok)     
                try: 
                    ScheduleType_data=request.data.get("ScheduleType")
                    schedule_type=Board.objects.get(type=ScheduleType_data)
                    
                    if not schedule_content:
                        schedule_content=Board.objects.create(type=ScheduleType_data)
                    schedule.ScheduleType = schedule_type
                    schedule.ScheduleContent = schedule_content
                    schedule.save()
                    
                    # idol.idol_schedules.add(schedule)
                except Board.DoesNotExist:
                    category_serializer=BoardSerializer(data=ScheduleType_data)
                    
                    if category_serializer.is_valid():
                        schedule_type=category_serializer.save()
                    else:
                        return Response(category_serializer.errors, status=HTTP_400_BAD_REQUEST)
                    schedule.ScheduleType=schedule_type
                    schedule.save()    
                
                idol.idol_schedules.add(schedule)
                if idol.idol_schedules:
                    idol.has_schedules=True  
                    idol.save()
        
        # 2. participant 에 있는 idol의 idol_schedules 필드에 자동으로 schedule추가(OK)
        # 3. particioant에 아이돌 이름을 입력하면, 해당하는 아이돌들이 participant field에  자동으로 선택되어 질 것(ok)
                for participant_data in request.data.get("participant"):
                    try:
                        
                        idol_name_en=participant_data.get("idol_name_en")
                        idol=Idol.objects.get(idol_name_en=idol_name_en)
                        schedule.participant.add(idol)
                        
                    except Idol.DoesNotExist:
                        idol_serializer=IdolDetailSerializer(data=participant_data)
                        if idol_serializer.is_valid():
                            idol=idol_serializer.save()
                        else:
                            return Response(idol_serializer.errors, status=HTTP_400_BAD_REQUEST)
                    idol.idol_schedules.add(schedule)
                    if idol.idol_schedules:
                        idol.has_schedules=True  
                        idol.save()
                return Response(ScheduleSerializer(schedule).data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    """
  {

        "ScheduleTitle": "아는 형님 녹화",
        "ScheduleType": {
            "type": "broadcast"
        },
        "location": "여의도 일산",
        "when": "2023-06-30T18:00:00",
        "participant": [
            {
                "idol_name_kr": "닝닝",
                "idol_name_en": "Ning Ning"
            },
            {
                "idol_name_kr": "카리나",
                "idol_name_en": "Karina"
            }
        ]
    }

    {
        "ScheduleTitle": "Music Bank 녹화",
        "ScheduleType": {
            "type": "broadcast"
          },
        "location": "여의도 일산",
        "when": "2023-07-13T18:00:00",
        "participant": [
            {
                "idol_name_kr": "혜원",
                "idol_name_en": "Belle"
            },
            {
                "idol_name_kr": "줄리 한",
                "idol_name_en": "Julie"
            },
            {
                "idol_name_kr": "원 하늘",
                "idol_name_en": "Ha Neul"
            },
           {
                "idol_name_kr": "나띠",
                "idol_name_en": "Natty"
            }
        ]
    }
    """

"""
class IdolSchedulesCategories(APIView):#[수정(OK)]
    
    # def get(self, request, idol_name_kr, categories):
    def post(self, request, idol_name_kr):
        # category_list = categories.split(",")  # 다중 카테고리를 콤마로 분리
        
        all_categories = ["broadcast", "event", "release", "buy", "congrats"]
        category_list = request.data.get("categories", all_categories)
        when= request.data.get("when")
        print("when", when)
        year, month =when.split("-")
        
        print("year:",type(year), "month:",type(month))

        #client에서 아무런 카테고리를 선택하지 않은경우 ~> 모든 카테고리 활성상태
        # print(category_list)
        
        if len(category_list)==0:#아아돌이 참여하는 모든 스케쥴 받아옴
            schedules = Schedule.objects.filter(
                participant__idol_name_kr=idol_name_kr,
                when__year=year,
                when__month=month
            )
        else:#검색
            schedules = Schedule.objects.filter(
                ScheduleType__type__in=category_list,
                participant__idol_name_kr=idol_name_kr,
                when__year=year,
                when__month=month
            )
        if not schedules.exists():#참여하고 있는 스케줄이 없는 경우 
            return Response([], status=HTTP_404_NOT_FOUND)
        
        serializer = ScheduleSerializer(schedules, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


{
  "categories": ["congrats", "broadcast"],
  "when":"2023-07"
} or
{"categories":[]}
"""

class ScheduleDate(APIView):
    def post(self, request, idol_name_en):
           
        # category_list = categories.split(",")  # 다중 카테고리를 콤마로 분리
        
        all_categories = ["broadcast", "event", "release", "buy", "congrats"]
        category_list = request.data.get("categories", all_categories)
        when= request.data.get("when")
        year, month, day = None, None, None
        
        if when:
            cnt=when.count("-")
            if cnt==2:
                date=datetime.strptime(when, "%Y-%m-%d")
                year=date.year
                month=date.month
                day=date.day
                print("year", year, "month", month)
                print("day", day)
            else:
                date=datetime.strptime(when, "%Y-%m")
                year=date.year
                month=date.month
                print("year", year, "month", month)            
        
        if len(category_list)==0:#아아돌이 참여하는 모든 스케쥴 받아옴
            schedules = Schedule.objects.filter(
                participant__idol_name_en=idol_name_en,
                when__year=year,
                when__month=month
            )
        else:#검색
            schedules = Schedule.objects.filter(
                ScheduleType__type__in=category_list,
                participant__idol_name_en=idol_name_en,
                when__year=year,
                when__month=month         
            )
        if day:
            schedules = schedules.filter(when__day=day)
        
        if not schedules.exists():#참여하고 있는 스케줄이 없는 경우 
            return Response([], status=HTTP_200_OK)
        
        serializer = ScheduleSerializer(schedules, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

"""
{
  "categories": ["congrats", "broadcast"],
  "when":"2023-07-16" or "2023-07"
} 
"""
class UpcomingSchedules(APIView):
    def get(self, request, idol_name_en):
        today = datetime.today()
        try:
            schedules = Schedule.objects.filter(
            participant__idol_name_en=idol_name_en,
            when__gte=today
            ).order_by("when")[:3]
            serializer = ScheduleSerializer(schedules, many=True)
        except schedules.DoesNotExist:
            return Response([], status=HTTP_200_OK)
        return Response(serializer.data, status=HTTP_200_OK)


class TopIdols(APIView):
    def get(self, request):
        top_idols = Idol.objects.order_by('-pickCount')[:6]# 상위 6명의 아이돌을 pickCount 기준으로 내림차순으로 정렬하여 가져옴
        # 상위 6명의 아이돌의 pickCount를 가져와서 리스트에 저장
        top_idols_info=[PickIdolSerializer(idol).data for idol in top_idols]
        return Response(top_idols_info, status=HTTP_200_OK)



class IdolPhotos(APIView):

    def get_object(self, pk):

        try:
            return Idol.objects.get(pk=pk)    
        except Idol.DoesNotExist:
            raise NotFound
        
    def post(self, request, pk):

        idol =self.get_object(pk)
        if not request.user.is_admin:   
            raise PermissionDenied
        serializer=PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo=serializer.save(idol=idol)
            serializer=PhotoSerializer(photo)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)