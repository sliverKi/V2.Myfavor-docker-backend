from django.urls import path
from . import views

urlpatterns = [
    path("", views.Idols.as_view(), name="idolList."),  #등록된 idolList {GET, POST}
    
    path("<str:idol_name_kr>/", views.IdolDetail.as_view(), name="get specific idol detail-info."),  #{get, post}
    path("<str:idol_name_kr>/schedules/", views.IdolSchedule.as_view(), name="create-idol-scheduel."), #{아이돌의 일정 생성, get,post}
    
    
    #[보류~> 다중 카테고리로 변경, 년월일 자를 같이 받아야]
    path("<str:idol_name_kr>/schedule/",views.IdolSchedulesCategories.as_view(), name="make multi category in idol schedules."), #{post}
    # path("<str:idol_name_kr>/schedules/<categories>",views.IdolSchedulesCategories.as_view()), #GET 수정OK
    
    path("<int:pk>/schedules/<str:type>/<str:year>/", views.IdolSchedulesYear.as_view()), 
    path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/", views.IdolSchedulesMonth.as_view()),  
    path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/<str:day>/", views.IdolScheduelsDay.as_view()), 

]

#pk->str로 변경