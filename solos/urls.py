from django.urls import path
from . import views

urlpatterns=[
    path("", views.SoloList.as_view()),
    path("<str:idol_name_kr>/", views.SoloDetail.as_view())
]
