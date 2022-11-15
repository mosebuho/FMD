from django.contrib import admin
from django.urls import path, include
from .views import HomeView, search
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view()),
    path("", include("allauth.urls")),
    path("search/", search, name="search"),
    path("user/", include("user.urls")),
    path("board/", include("board.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
