from django.urls import path
from . import views
urlpatterns=[
    path("<str:groupname>",views.GroupAlbum.as_view()),#get, post
    path("<str:groupname>/<int:pk>", views.GroupAlbumDetail.as_view()),#get, put,delete
    path("<str:idol_name_en>/", views.SoloAlbum.as_view()),#get, post
    path("<str:idol_name_en>/a/<int:pk>", views.SoloAlbumDetail.as_view()),#get,put,delete
]