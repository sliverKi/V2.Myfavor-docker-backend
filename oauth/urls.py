from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from . import views
urlpatterns=[
    path("email/", views.emailValidate.as_view(), name="email_authentication"),
    path("login/", views.Login.as_view(), name="try_login"),  
    path("logout/", views.Logout.as_view()),  
    path("findID/", views.FindID.as_view()),
    path("findPW/", views.FindPW.as_view()),# 수정 필요함 
    path("reset/<pk>/<token>/", views.PWResetConfirm.as_view(), name='password_reset'),
    path("changePW/", views.ChangePW.as_view()),  
   
]
