from tokenize import generate_tokens
from django.conf import settings
from django.db import transaction
from django.db.models import Q

from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    
)
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import User, Report
from .serializers import (
    SimpleUserSerializers,
    TinyUserSerializers,
    PrivateUserSerializer,
    ReportDetailSerializer,
    UserSerializer,
    PickSerializer,
)
from medias.serializers import UserProfileSerializer
from idols.models import Idol


class LoginUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user
        print("user: ", user)
        serializer=TinyUserSerializers(user)
        return Response(serializer.data, status=HTTP_200_OK)
    

class AllUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):  
        all_users = User.objects.all()  
        serializer = UserSerializer(
            all_users,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)

class MyPage(APIView):  
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = TinyUserSerializers(user)
        return Response(serializer.data, status=HTTP_200_OK)

    
    def put(self, request):
        user = request.user
        serializer = TinyUserSerializers(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)



class UserDetail(APIView):  
    # permission_classes = [IsAdminUser]  

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

   
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = TinyUserSerializers(
            user,
            data=request.data,
            partial=True,
        )
        print("re", request.data)
        if serializer.is_valid():
            print(1)
            user = serializer.save()
            print(2)
            serializer = TinyUserSerializers(user)
            print(3)
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

  
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


class EditPick(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request):
        pick = request.user
        serializer = PickSerializer(pick)
        return Response(serializer.data, status=HTTP_200_OK)


    def put(self, request):
        user = request.user
        print("me",user)
        serializer = PickSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_pick = serializer.save()
            return Response(PickSerializer(updated_pick).data, status=HTTP_202_ACCEPTED)



class AllReport(APIView):
    def get(self, request):#[수정 ok]

        all_reports = Report.objects.all()
        serializer = ReportDetailSerializer(all_reports, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self,request):#[수정 ok]
        user=request.user
        print("0",user.pick)
        serializer = ReportDetailSerializer(
            data=request.data,  
        )
        if serializer.is_valid():
            report=serializer.save(
                owner=user.nickname,
                
                ScheduleType=request.data.get("ScheduleType"),
            )
            serializer=ReportDetailSerializer(
                report, 
                context={"request":request}
            )
            return Response(serializer.data, HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ReportDetail(APIView):
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        report = self.get_object(pk)
        serializer = ReportDetailSerializer(report)
        return Response(serializer.data, status=HTTP_200_OK)

    

    def put(self, request, pk):
        if not request.user.is_admin:
            raise PermissionDenied("권한 없음")
        else:
            report = self.get_object(pk)
            serializer = ReportDetailSerializer(
                report,
                data=request.data,
                partial=True,
            )
        if serializer.is_valid():
            updated_report = serializer.save(
                ScheduleType=request.data.get("ScheduleType"),
                whoes=request.data.get("whoes"),
                location=request.data.get("location")
            )
            return Response(
                ReportDetailSerializer(updated_report).data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reports = self.get_object(pk)

        if not request.user.is_admin:
            raise PermissionDenied

        reports.delete()

        return Response(status=HTTP_204_NO_CONTENT)

class MyReport(APIView):#내가 제보한 글
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user

        user_report=Report.objects.filter(owner=user).order_by('-created_at')
        serializer=ReportDetailSerializer(user_report, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class MyReportDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound
    
    def get(self, reqeust, pk):
        report=self.get_object(pk)
        serializer=ReportDetailSerializer(report)
        return Response(serializer.data, status=HTTP_200_OK)
        
    def put(self, request, pk):
        report=self.get_object(pk)
        
        if report.is_enroll:
            return Response({"message":"이 제보는 등록되었습니다.!"}, status=HTTP_400_BAD_REQUEST)
        
        serializer=ReportDetailSerializer(
            report, 
            data=request.data, 
            partial=True, 
        )
        if serializer.is_valid():
            updated_report=serializer.save(
                ScheduleType=request.data.get("ScheduleType"),
                whoes=request.data.get("whoes")
            )
            serializer=ReportDetailSerializer(updated_report)
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        reports = self.get_object(pk)
        reports.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class UserPhotos(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)    
        except User.DoesNotExist:
            raise NotFound
    
    def post(self, request, pk):
        idol =self.get_object(pk)
        serializer=UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            photo=serializer.save(idol=idol)
            serializer=UserProfileSerializer(photo)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

