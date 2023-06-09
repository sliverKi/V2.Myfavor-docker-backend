from django.urls import path
from . import views
urlpatterns=[
    path("<str:groupname>",views.GroupAlbum.as_view()),
    path("<str:groupname>/<int:pk>", views.GroupAlbumDetail.as_view()),
    path("<str:idol_name_kr>/", views.SoloAlbum.as_view()),
    path("<str:idol_name_kr>/a/<int:pk>", views.SoloAlbumDetail.as_view()),
]