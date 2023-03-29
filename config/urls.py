from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/idols/", include("idols.urls")),
    path("api/v1/media/", include("media.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/users_calendar/", include("usersCalendar.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
