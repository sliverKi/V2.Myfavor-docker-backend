from django.urls import path
from . import views
urlpatterns=[
    path("", views.IdolsHits.as_view()),
    path("<str:idol_name_kr>", views.TopIdol.as_view())
]