from django.urls import path
from . import views

urlpatterns=[
    path("", views.SoloList.as_view()),
]