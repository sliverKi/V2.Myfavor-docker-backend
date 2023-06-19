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
from .serializers import  TinyIdolSerializer, IdolsListSerializer, IdolDetailSerializer, DateScheduleSerializer

from categories.serializers import CategorySerializer
from categories.models import Category
from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule
from medias.serializers import PhotoSerializer
from groups.models import Group
class Idols(APIView): #[수정OK]
    
    def get(self, request):

        all_idols = Idol.objects.all()
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



class IdolDetail(APIView): #[수정OK]

    def get_object(self, idol_name_kr): 
        try:
            return Idol.objects.get(idol_name_kr=idol_name_kr)
        except Idol.DoesNotExist:
            raise NotFound

    def get(self, request, idol_name_kr): 
        idol = self.get_object(idol_name_kr)
        serializer = IdolDetailSerializer(
            idol,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, idol_name_kr): 
        if not request.user.is_admin:
            raise PermissionDenied

        idol=self.get_object(idol_name_kr)
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
            "idol_debut":"2020-11-17",
            "idol_birthday":"2001-01-01", 
            "idol_profile":"https://i.namu.wiki/i/j1mSQz1rUEGD8yslNgSdyWgHTaMeVMP0T6z45HuNUoKXSg3XZ92sQOeWKRI4bUEwCyy0YaI-tPrGEEhEIZlrSrZM4WA2qy0TvYL_TC6X6x79QowHTp8h6ECieB24d3TybWT5VZvF7X66cf86yI48gg.webp"
        }
        """

    def delete(self, request, idol_name_kr): 
        idol=self.get_object(idol_name_kr)
       
        if request.user.is_admin==False: 
            raise PermissionDenied
        idol.delete()
        if idol.DoesNotExist:
            return Response(status=HTTP_204_NO_CONTENT)    

class IdolSchedule(APIView): #수정[OK]

    def get_object(self, idol_name_kr):

        try:
            return Idol.objects.get(idol_name_kr=idol_name_kr)
        except Idol.DoesNotExist:
            raise NotFound

    def get(self, request, idol_name_kr):

        idol = self.get_object(idol_name_kr)
        serializer = ScheduleSerializer(
            
            idol.idol_schedules.all(),
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)

    
    def post(self, request, idol_name_kr):
        #아이돌 스케줄이 등록되면 hasSchedule을 false에서 true로 변경 할 것 (participant 에 있는 아이들도 같이 바꿀것 )
        idol=self.get_object(idol_name_kr)
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
                    schedule_type=Category.objects.get(type=ScheduleType_data)
                    
                    if not schedule_content:
                        schedule_content=Category.objects.create(type=ScheduleType_data)
                    schedule.ScheduleType = schedule_type
                    schedule.ScheduleContent = schedule_content
                    schedule.save()
                    
                    # idol.idol_schedules.add(schedule)
                except Category.DoesNotExist:
                    category_serializer=CategorySerializer(data=ScheduleType_data)
                    
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
                        
                        idol_name_kr=participant_data.get("idol_name_kr")
                        idol=Idol.objects.get(idol_name_kr=idol_name_kr)
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
            "type": "broadcast",
            "content":"지젤 건강문제로 녹화 불참"(optional)
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
    """



class SearchIdol(APIView):
    def get(self, request):
        idol_name=request.GET.get('idol_name')
        if idol_name:
            idols=Idol.objects.filter(idol_name_kr__icontains=idol_name) 
        else:
            return Response({"message":"해당 아이돌이 존재하지 않습니다."})
        serializer=TinyIdolSerializer(idols, many=True)
        return Response(serializer.data, status=HTTP_200_OK)



        
          
class IdolSchedulesCategories(APIView):#[수정(OK)]
    
    def get_object(self, idol_name_kr):
        
        try:
            return Idol.objects.get(idol_name_kr=idol_name_kr)        
        except Idol.DoesNotExist:
            raise NotFound
        
    def get(self, request, idol_name_kr,  type):
        
        idol=self.get_object(idol_name_kr)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type).order_by("when")
        
        filter_schedules=[]
        for s in schedules:
            if s.ScheduleType and s.ScheduleType.type==type:
                filter_schedules.append(s)

        serializer=ScheduleSerializer(filter_schedules, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class IdolSchedulesYear(APIView):
    
    def get_object(self, pk):
        
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            return NotFound
    
    def get(self, request, pk, type, year):
        
        idol=self.get_object(pk=pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type, when__year=year)
        serializer=DateScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK) 

class IdolSchedulesMonth(APIView):
    
    def get_object(self, pk):
        
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            return NotFound
    
    def get(self, request, pk, type, year, month):
        
        idol=self.get_object(pk=pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type, when__year=year, when__month=month)
        serializer=DateScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK) 


class IdolScheduelsDay(APIView):
    
    def get_object(self, pk):

        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            return NotFound
    
    def get(self, request, pk, type, year, month, day):

        idol=self.get_object(pk=pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type, when__year=year, when__month=month, when__day=day)
        
        serializer=DateScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK) 

    

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