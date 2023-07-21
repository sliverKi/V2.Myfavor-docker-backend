from django.urls import path

from . import views


urlpatterns = [

    
    path("me/",views.LoginUser.as_view(), name="loginSuccess_user's_info"),
    path("list/", views.AllUsers.as_view()),  
    path("mypage/", views.MyPage.as_view()), 
    
    path("<int:pk>/", views.UserDetail.as_view()),  
    path("edit/pick/", views.EditPick.as_view()),  
    
    path("reports/", views.AllReport.as_view()),#[get, post] :user can report idol schedule.
    path("reports/<int:pk>/", views.ReportDetail.as_view()),#[get, put, delete] # admin user modified or register user's report.
    
    path("mypage/myreport/", views.MyReport.as_view()), # get
    path("mypage/myreport/<int:pk>", views.MyReportDetail.as_view()),#get,put,delete : user
    
]

#{"email":"myfavor@gmail.com","passsword":"myfavor"}
#{"email":"test123@gmail.com","password":"test123@E"}
#{"email":"test123@gmail.com", "password":"test123@E", "age":"30", "pick":1, "name":"md", "phone":"010-1234-5678", "nickname":"test"}