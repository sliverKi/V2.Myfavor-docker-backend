from django.urls import path
from .views import GetUploadURL
from .views import PhotoDetail

urlpatterns=[
    path("photos/<int:pk>/", PhotoDetail.as_view()),
    path("photos/get-url/", GetUploadURL.as_view()),
    # path("photos/get-s3/", GetS3URL.as_view()),
]