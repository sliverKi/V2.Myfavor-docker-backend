from django.urls import path
from . import views

urlpatterns=[
    path("", views.SoloList.as_view()),#[get, post]
    path("<str:idol_name_en>/", views.SoloDetail.as_view())#[get, put, delete]
]
