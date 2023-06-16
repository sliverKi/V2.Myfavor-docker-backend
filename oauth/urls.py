from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from . import views
urlpatterns=[
    path("login/", views.Login.as_view()),  
    path("logout/", views.Logout.as_view()),  
    path("findID/", views.FindID.as_view()),
    path("findPW/", views.FindPW.as_view()),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("changePW/", views.ChangePW.as_view()),  
]
