from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from . import views
urlpatterns=[
    path("login/", views.Login.as_view()),  
    path("logout/", views.Logout.as_view()),  
    path("findID/", views.FindID.as_view()),
    path("findPW/", views.FindPW.as_view()),# 수정 필요함 
    path("reset/<pk>/<token>/", views.PWResetConfirm.as_view(), name='password_reset'),
    path("changePW/", views.ChangePW.as_view()),  
    # path("changePW/done", views.confirmChangePW.as_view())
]
