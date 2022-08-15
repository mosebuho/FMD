from django.contrib import admin
from django.urls import path, include
from .views import HomeView, Home2View
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view()),
    path("home2/", Home2View.as_view()),
    path("user/", include("user.urls")),
    path("board/", include("board.urls")),
    path("summernote/", include("django_summernote.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
