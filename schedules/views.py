from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,PermissionDenied,ParseError
from .models import Schedule
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_202_ACCEPTED, 
    HTTP_204_NO_CONTENT, 
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN, 
    HTTP_404_NOT_FOUND 
)
from .serializers import  slideScheduleSerializer, ScheduleSerializer, ScheduleDetailSerializer
from datetime import datetime
class Schedules(APIView): 
    
    def get(self, request):
        all_schedules = Schedule.objects.all().order_by("pk")
        print(all_schedules)
        serializer = ScheduleSerializer(all_schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
  
        if not request.user.is_admin:
            raise PermissionDenied
        else:
            serializer = ScheduleDetailSerializer(data=request.data)
            print("re",request.data)
            if serializer.is_valid():
                schedule = serializer.save(
                    ScheduleType=request.data.get("ScheduleType"),
                    participant=request.data.get("participant")
                )
                serializer=ScheduleDetailSerializer(
                    schedule,
                    context={'request':request}
                )
                return Response(serializer.data, HTTP_201_CREATED )
            else:
                return Response(serializer.errors, HTTP_403_FORBIDDEN)


class SlideSchedules(APIView):
    def get(self, pk):
        today=datetime.today()
        print(today)
        slide_schedules = Schedule.objects.filter(
            when__gte=today
        ).order_by("when")
        serializer = slideScheduleSerializer(slide_schedules, many=True)
        
        modified_data = []#participant가 다수의 아이돌을 포함하고 있는 경우 ~> 쪼개기
        for entry in serializer.data:
            for participant in entry["participant"]:
                new_entry = entry.copy()
                new_entry["participant"] = participant
                if not len(modified_data)==10:
                    modified_data.append(new_entry)
                else:
                    break
        return Response(modified_data, status=HTTP_200_OK)
        # return Response(serializer.data, status=HTTP_200_OK)
            

class ScheduleDetail(APIView): 

    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = ScheduleDetailSerializer(schedule)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):#type, participant도 변경할 수 있게 해야함
        if not request.user.is_admin:
            raise PermissionDenied
        
        if request.user.is_admin:
            schedule = self.get_object(pk)
            serializer = ScheduleDetailSerializer(
                schedule,
                data=request.data,
                partial=True,
            )
            print("re",request.data)
            if serializer.is_valid():
                updated_schedule = serializer.save(
                    ScheduleTitle=request.data.get("ScheduleTitle"),
                    ScheduleType=request.data.get("ScheduleType"),
                    location=request.data.get("location"),
                    when=request.data.get("when"),
                    participant=request.data.get("participant")
                )
                return Response(ScheduleDetailSerializer(updated_schedule).data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        schedule = self.get_object(pk)
        if not request.user.is_admin:
            return PermissionDenied
        schedule.delete()
        return Response(status=HTTP_204_NO_CONTENT)