from django.contrib import admin
from django.urls import path, include
from .views import HomeView, search
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from sitemaps import NewsSitemap, ColumnSitemap, CommunitySitemap
from django.views.generic import TemplateView

sitemaps = {
    "news": NewsSitemap,
    "column": ColumnSitemap,
    "community": CommunitySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("", include("allauth.urls")),
    path("search/", search, name="search"),
    path("user/", include("user.urls")),
    path("board/", include("board.urls")),
    path("sitemap.xml/", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('robots.txt/',  TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
