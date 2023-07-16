from . import views
from django.urls import path
urlpatterns=[
    path("", views.GroupList.as_view()),#[get[=등록되어진 아이돌 그룹]/post(검색시 이용)]
    path("<str:groupname>", views.GroupDetail.as_view()),# get, put, delete
    path("<str:groupname>/<str:idol_name_en>", views.GroupIdol.as_view()),#get, delete
]
#[group page complete]