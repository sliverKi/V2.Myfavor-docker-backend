from django.urls import path
from . import views

urlpatterns = [
    path("", views.Idols.as_view(), name="idolList."),  #등록된 idolList {GET, POST}
    path("rank/", views.TopIdols.as_view(), name="Not Found Page"),
    path("<str:idol_name_en>/", views.IdolDetail.as_view(), name="get specific idol detail-info."),  #{get, post}
    path("<str:idol_name_en>/schedules/", views.enrollIdolSchedule.as_view(), name="enroll_idol_scheduel.(by admin user)"), #{get,post}

    
    path("<str:idol_name_en>/schedule/", views.ScheduleDate.as_view(), name="filter_schedule_by_date"),
    path("<str:idol_name_en>/upcoming/",views.UpcomingSchedules.as_view(), name="upcoming-schedules"),    
]

#pk->str로 변경

# path("<str:idol_name_en>/schedules/", views.IdolSchedule.as_view(), name="enroll_idol_scheduel.(by admin user)"), #{get,post}