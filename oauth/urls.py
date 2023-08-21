from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from . import views
urlpatterns=[
    path("signup/step1/", views.step1_SignUP.as_view(), name="email_signUp_step1"),
    path("vertify/<pk>/<token>/", views.EmailVerification.as_view(), name="email_verification"),
    path("signup/step2/<pk>/<token>/", views.step2_SignUp.as_view(), name="email_signUp_step2"),
    
    path("login/", views.Login.as_view(), name="try_login"),  
    path("logout/", views.Logout.as_view()),  
    
    path("findID/", views.FindID.as_view()),
    path("findPW/", views.FindPW.as_view()),
    path("reset/<pk>/<token>/", views.PWResetConfirm.as_view(), name='password_reset'),
    path("changePW/", views.ChangePW.as_view()),  
]
