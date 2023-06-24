from django.urls import path
from . import views
urlpatterns=[
    path("like/<str:idol_name_kr>", views.IdolLike.as_view())
]