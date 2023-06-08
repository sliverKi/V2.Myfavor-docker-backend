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
from .serializers import ScheduleSerializer

# Create your views here.
class Schedules(APIView): 
    
    def get(self, request):
        print(0)
        all_schedules = Schedule.objects.all()
        print(all_schedules)
        serializer = ScheduleSerializer(all_schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
  
        if not request.user.is_admin:
            raise PermissionDenied
        else:
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                schedule = serializer.save()
                return Response(ScheduleSerializer(schedule).data, HTTP_201_CREATED )
            else:
                return Response(serializer.errors, HTTP_403_FORBIDDEN)


class ScheduleDetail(APIView): 

    def get_object(self, pk):

        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise NotFound

    def get(self, request, pk):

        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):#type, participant도 변경할 수 있게 해야함
        
        if not request.user.is_admin:
            raise PermissionDenied
        
        if request.user.is_admin:
            schedule = self.get_object(pk)
            serializer = ScheduleSerializer(
                schedule,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                updated_schedule = serializer.save(
                    ScheduleType=request.data.get("ScheduleType"),
                    participant=request.data.get("participant")
                )
                return Response(ScheduleSerializer(updated_schedule).data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        schedule = self.get_object(pk)
        if not request.user.is_admin:
            return PermissionDenied
        schedule.delete()
        return Response(status=HTTP_204_NO_CONTENT)