from django.urls import path
from . import views
urlpatterns=[
    path("login/", views.Login.as_view()),  
    path("logout/", views.Logout.as_view()),  
    path("findID/", views.FindID.as_view()),
    # path("findPW/", views.FindPW.as_view())
    path("edit/password/", views.EditPassword.as_view()),  
]
