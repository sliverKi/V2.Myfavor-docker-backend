from django.shortcuts import render
from django.contrib.auth import login, logout

from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from users.models import User
from users.serializers import (
    TinyUserSerializers
)
from .serializers import FindIDSerializer

class Login(APIView):  
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound
        
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        
        if user.check_password(password):
            login(request, user)
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class Logout(APIView):  
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "See You Again~"}, status=status.HTTP_200_OK)
    

class FindID(APIView):
#input data:  {"nickname":"관리자", "phone":"010-3578-8072"}
    def post(self, request):
        nickname=request.data.get("nickname")
        phone=request.data.get("phone")
        if not nickname or not phone:
            raise ParseError("Please, insert data.")
        try:
            user = User.objects.get(nickname=nickname, phone=phone)
            print("user: ", user)
            email = user.email
            return Response({"ID": email}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "This information does not exist. Are you our member?"}, status=status.HTTP_404_NOT_FOUND)

class FindPW(APIView):

    def post(self, request):#닉네임 이메일 전화번호
        nickname=request.data.get("nickname")
        email=request.data.get("email")
        phone=request.data.get("phone")

        if not nickname or not email or not phone:
            raise ParseError("Please, insert data.")
        try:
            user=User.objects.get(nickname=nickname, email=email, phone=phone)
            print("User: ", user)
            
            




class EditPassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            if old_password != new_password:
                user.set_password(new_password)
                user.save()
                return Response({"비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"변경 될 비밀번호가 기존 비밀번호와 동일합니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ParseError("비밀번호를 다시 확인해주세요.")
