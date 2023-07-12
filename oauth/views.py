from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
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

from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class emailValidate(APIView):
    def get(self, request):
        return Response({"message":"이메일 인증을 완료해 주세요."}, status=status.HTTP_200_OK)
    def post(self, request):
        pass

class Login(APIView):  
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(
            request,
            email = email,
            password = password,
        )    
            
        except User.DoesNotExist:
            raise NotFound
        
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        
        if user.check_password(password):
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response({"error": "비밀번호가 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
#접속한 사용자의 정보를 불러와야 함.
#{"email":"myfavor@gmail.com", "password":"myfavor"}

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

class FindPW(APIView):#비밀번호 잊으면 비밀번호 초기화-> 재설정-> 로그인 뷰로 라다이렉트
# {"nickname":"관리자", "email":"myfavor@gmail.com", "phone":"010-3578-8072"}

    def post(self, request):#닉네임 이메일 전화번호
        nickname=request.data.get("nickname")
        email=request.data.get("email")
       

        # if not nickname or email:
        #     raise ParseError("Please, insert data.")
        try:
            user = User.objects.get(nickname=nickname, email=email)
            print(1)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate token for password reset link
        token_generator = default_token_generator
        token = token_generator.make_token(user)

        # Build password reset URL
        reset_url = request.build_absolute_uri(
            reverse_lazy("password_reset", kwargs={"pk": user.pk, "token": token})
        )#send mail 성공시 password_reset_confirm view로 이동 (redirect)

        # Email subject and message
        subject = "Password Reset"
        message = f"Please click the link below to reset your password:\n\n{reset_url}"
        # Send email
        send_mail(
            subject,
            message,
            "myfavor86@gmail.com",
            ["lovee2756@naver.com"],
            fail_silently=False,
        )

        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)

class PWResetConfirm(APIView):
    def post(self, request, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found.")
   
        # 단계 1: Base64로 인코딩된 사용자 ID를 디코딩합니다.
        #{"email":"lovee2756@naver.com", "nickname":"aaa"}
       
        # 단계 2: 비밀번호 재설정 토큰의 유효성을 확인합니다.
        token_generator = default_token_generator
        if not token_generator.check_token(user, token):
            raise NotFound("Invalid password reset token.")

        # 단계 3: 새로운 비밀번호를 업데이트합니다.
        new_password = request.data.get("new_password")
        print("4", new_password)#{"new_password":"eungi123@E"}
        if not new_password:
            return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)


            




class ChangePW(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")#{"eungi123@E"}
        new_password = request.data.get("new_password")#{"eungi135@E"}

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

