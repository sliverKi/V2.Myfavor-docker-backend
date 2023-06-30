from django.urls import path
from . import views

urlpatterns = [
    path("", views.Schedules.as_view()), #등록된 schedule list get, post}
    path("<int:pk>/", views.ScheduleDetail.as_view()), #등록된 schedule 수정 {get, put , delete}
]