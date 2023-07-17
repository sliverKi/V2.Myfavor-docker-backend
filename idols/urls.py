from django.urls import path
from . import views

urlpatterns = [
    path("", views.Idols.as_view(), name="idolList."),  #등록된 idolList {GET, POST}
    path("topIdol/", views.TopIdols.as_view()),
    path("<str:idol_name_en>/", views.IdolDetail.as_view(), name="get specific idol detail-info."),  #{get, post}
    path("<str:idol_name_en>/schedules/", views.IdolSchedule.as_view(), name="create-idol-scheduel."), #{아이돌의 일정 생성, get,post}
    
    
    #[보류~> 다중 카테고리로 변경, 년월일 자를 같이 받아야-> 해결: ScheduleDate]
    # 필요 없는 url -> path("<str:idol_name_kr>/schedule/",views.IdolSchedulesCategories.as_view(), name="make multi category in idol schedules."), #{post}
    path("<str:idol_name_en>/schedule/", views.ScheduleDate.as_view(), name="filter_schedule_date"),
    path("<str:idol_name_en>/upcoming/",views.UpcomingSchedules.as_view(), name="upcoming-schedules"),    
    
    #아래 url 다 필요 없음
    # path("<str:idol_name_kr>/schedules/<categories>",views.IdolSchedulesCategories.as_view()), #GET 수정OK
    
    # path("<int:pk>/schedules/<str:type>/<str:year>/", views.IdolSchedulesYear.as_view()), 
    # path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/", views.IdolSchedulesMonth.as_view()),  
    # path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/<str:day>/", views.IdolScheduelsDay.as_view()), 

]

#pk->str로 변경