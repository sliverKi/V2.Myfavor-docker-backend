from django.urls import path

from . import views


urlpatterns = [

    path("", views.NewUsers.as_view()),  
    path("me/",views.LoginUser.as_view(), name="loginSuccess_user's_info"),
    path("list/", views.AllUsers.as_view()),  
    path("mypage/", views.MyPage.as_view()), 
    path("mypage/myreport/", views.MyReport.as_view()), 
    path("<int:pk>/", views.UserDetail.as_view()),  
    path("edit/pick/", views.EditPick.as_view()),  
    path("reports/", views.AllReport.as_view()),#[get, post]
    path("reports/<int:pk>/", views.ReportDetail.as_view()),#[get, put, delete]

    
]

#{"email":"myfavor@gmail.com","passsword":"myfavor"}
#{"email":"test123@gmail.com","password":"test123@E"}
#{"email":"test123@gmail.com", "password":"test123@E", "age":"30", "pick":1, "name":"md", "phone":"010-1234-5678", "nickname":"test"}