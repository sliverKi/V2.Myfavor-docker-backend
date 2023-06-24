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

class NewUsers(APIView):
    def get(self, request):
        return Response({"email, password, nickname, age, pick, phone 을 입력해주세요."})

    def post(self, request):

        password = request.data.get("password")

        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        print(password)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data)

    
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
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)

class MyReport(APIView):#내가 제보한 글 도 볼 수 있게 
    permission_classes = [IsAuthenticated]
    def get(self, pk):
        pass

class UserDetail(APIView):  
    permission_classes = [IsAdminUser]  

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
        if serializer.is_valid():
            user = serializer.save()
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=HTTP_200_OK)
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
        return Response(serializer.data)


    def put(self, request):
        pick = request.user

        serializer = PickSerializer(
            pick,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_pick = serializer.save()
            return Response(PickSerializer(updated_pick).data)



class AllReport(APIView):
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request):#[수정 ok]

        all_reports = Report.objects.all()
        serializer = ReportDetailSerializer(all_reports, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self,request):#[수정 ok]

        serializer = ReportDetailSerializer(
            data=request.data,
            
        )
        if serializer.is_valid():
            with transaction.atomic():
                owner_nickname = request.user.nickname
                owner = User.objects.get(nickname=owner_nickname)
                report = serializer.save(owner=owner)
                whoes = request.data.get("whoes", [])
                
                print("whoes",whoes)
                print(request.user.pick.idol_name_en)
                if not whoes:
                    raise ParseError("제보할 아이돌을 알려 주세요.")
                if len(set(whoes)) != 1:
                    raise ParseError("한명의 아이돌만 제보가 가능합니다.")
                if not any(
                    request.user.pick.idol_name_kr in whoes_item or
                    request.user.pick.idol_name_en in whoes_item
                    for whoes_item in whoes
                    ):
                    raise ParseError("참여자는 본인의 아이돌만 선택 가능합니다.")
                if not isinstance(whoes, list):
                    if whoes:
                        raise ParseError("who_pk must be a list")
                    else:
                        raise ParseError(
                            "whoes report? Who should be required. not null"
                        )
                idol_name = whoes[0].split("(")[0].strip()
               
                try:
                    idol = Idol.objects.get(Q(idol_name_kr=idol_name) | Q(idol_name_en=idol_name))
                    report.whoes.add(idol)

                except Idol.DoesNotExist:
                    raise ParseError("선택하신 아이돌이 없어요.")

                serializer = ReportDetailSerializer(
                    report,
                    context={"request": request},
                )
                return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
"""
{
    "whoes": ["Winter"], ["윈터(Winter)"], ["윈터"]
    "type": "broadcast",
    "content": "Billboard Show Case2",
    "title": "2227",
    "location": "USA",
    "time": "2023-03-12T15:34:03+09:00"
}
"""

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
            updated_report = serializer.save()
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

