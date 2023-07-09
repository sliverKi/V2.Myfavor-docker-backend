from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v2/board/", include("boards.urls")),
    path("api/v2/idols/", include("idols.urls")),
    path("api/v2/medias/", include("medias.urls")),
    path("api/v2/users/", include("users.urls")),
    path("api/v2/users_calendar/", include("usersCalendar.urls")),
    path("api/v2/groups/", include("groups.urls")),
    path("api/v2/schedules/", include("schedules.urls")),
    path("api/v2/oauth/", include("oauth.urls")),
    path("api/v2/search/", include("search.urls")),
    path("api/v2/solos/", include("solos.urls")),
    path("api/v2/hits/", include("hits.urls")),
    path("api/v2/albums/", include("albums.urls")),
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns +=[
        path('__debug__/', include(debug_toolbar.urls)),
    ]