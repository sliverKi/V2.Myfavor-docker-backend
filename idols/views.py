from django.shortcuts import render, get_object_or_404
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
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Idol
from .serializers import  IdolsListSerializer, IdolDetailSerializer, PickIdolSerializer
from boards.models import Board
from boards.serializers import BoardSerializer
from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule
from medias.serializers import PhotoSerializer
from groups.models import Group
from users.models import User
from datetime import datetime
from django.core.cache import cache
import logging
from config.settings import DEBUG
class getIdol:
    def get_idol(self, idol_name_en): 
        try:
            return Idol.objects.get(idol_name_en=idol_name_en)
        except Idol.DoesNotExist:
            raise NotFound
        
class Idols(APIView): #[수정OK, testOK]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        if DEBUG:
            cache_key="idols-List"
            cached_data=cache.get(cache_key)
            #Cache Hit
            if cached_data:
                logger=logging.getLogger(__name__)
                logger.info(f"Cache HIT for idol key :{cache_key}")
                return Response(cached_data, status=HTTP_200_OK)
             #Cache Miss
            all_idols = Idol.objects.prefetch_related().order_by("pk")
            serializer = IdolsListSerializer(all_idols, many=True)
            cache.set(cache_key, serializer.data, 60 * 30)  #Cache Keep
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            all_idols = Idol.objects.prefetch_related().order_by("pk")
            serializer = IdolsListSerializer(all_idols, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):  
        if not request.user.is_admin: 
            raise PermissionDenied
        is_solo = request.data.get('is_solo') 
        print("is_solo", is_solo)
        serializer = IdolDetailSerializer(data=request.data)
        if serializer.is_valid():
            idol = serializer.save(is_solo=is_solo)
            # Delete the existing cache, if new idol is successfully saved
            cache_key = "idols-List"
            cache.delete(cache_key)
            return Response(IdolsListSerializer(idol).data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    """
    post input data
        {
            "idol_name_kr":"선미",
            "idol_name_en":"SunMi",
            "idol_profile":"https://i.namu.wiki/i/OsLvNXbYOYIMIe8ttpDZn1jLL0JL3RFZmZcmAWXMvcg7hYvHtX8Np4njdPC5SVlugrL6fjRyLZd_Prk-h9BB2v13y-dtP7eQKaKkcWTXNq21M6m2D0rpYLTfW1NsYhVXFB5fyOF4XdqMtU4UWwxCiQ.webp",
            "idol_birthday":"1992-05-02",
            "is_solo":"True"
        }
    """



class IdolDetail(getIdol, APIView): #[수정OK]
    permission_classes = [IsAuthenticatedOrReadOnly]
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

class IdolSchedule(getIdol, APIView): #[페기]

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
        if not request.user.is_admin:
            raise PermissionDenied
        serializer=ScheduleSerializer(data=request.data)
        print("re", request.data)
        if serializer.is_valid():
            schedule = serializer.save()  
            try: 
                ScheduleType_data=request.data.get("ScheduleType")
                schedule_type=Board.objects.get(type=ScheduleType_data)
                print("1", schedule_type)
                schedule.ScheduleType = schedule_type
                schedule.participant.add(idol)
                schedule.save()
                idol.idol_schedules.add(schedule)
                if idol.idol_schedules:
                    idol.has_schedules=True  
                    idol.save()
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
                return Response(ScheduleSerializer(schedule).data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
       

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
class UpcomingSchedules(APIView):#다가올 스케쥴
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


class TopIdols(APIView):#get
    def get(self, request):
        top_idols = Idol.objects.order_by('-pickCount')[:4]# 상위 6명의 아이돌을 pickCount 기준으로 내림차순으로 정렬하여 가져옴
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
        
class enrollIdolSchedule(getIdol, APIView):
    
    def get(self, request, idol_name_en):
        idol = self.get_idol(idol_name_en)
        serializer = ScheduleSerializer(
            
            idol.idol_schedules.all(),
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, idol_name_en):
        if not request.user.is_admin:
            return Response({"error":"관리자만이 아이돌 스케쥴 등록 가능"}, status=HTTP_403_FORBIDDEN)
        idol = get_object_or_404(Idol, idol_name_en=idol_name_en)
        print("1", idol)
        serializer=ScheduleSerializer(data=request.data)
        owner_name=request.data.get("owner")
        schedule_type=request.data.get("ScheduleType")
        print("owner", owner_name, "schedule_type", schedule_type)
        try:
            owner=User.objects.get(name=owner_name)
            schedule_type=Board.objects.get(type=schedule_type)
            print("1", schedule_type, owner.nickname)
        except User.DoesNotExist:
            return Response({"error":"제보 작성자가 존재하지 않음."}, status=HTTP_404_NOT_FOUND)
        except Board.DoesNotExist:
            return Response({"error":"schedule_type이 유효하지 않음."}, status=HTTP_404_NOT_FOUND)
        participant = request.data.get("participant")
        print("participant", participant[0])

        if not Idol.objects.filter(idol_name_en=participant[0]).exists():
            print("x")
            return Response(
                {"error": f"The following idols in 'participant' field are invalid: {', '.join(participant)}"},
                status=HTTP_400_BAD_REQUEST
            )
        print("O")
        if serializer.is_valid():
            schedule=Schedule.objects.create(
                owner=owner,
                ScheduleType=schedule_type,
                ScheduleTitle=request.data.get("ScheduleTitle"),
                location=request.data.get("location"),
                when=request.data.get("when")
            )
            schedule.participant.add(idol)
            idol.idol_schedules.add(schedule)
            schedule.save()
            idol.save()
            return Response(ScheduleSerializer(schedule).data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


        
""" 
{
    "owner":"관리자",
    "ScheduleType": "broadcast",
    "ScheduleTitle": "report test2 ",
    "location": "Seoul",
    "when": "2023-07-25T06:34:03+09:00",
    "participant":["JENNY"]
}
"""
