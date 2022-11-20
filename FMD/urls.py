from django.contrib import admin
from django.urls import path, include
from .views import HomeView, search

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("", include("allauth.urls")),
    path("search/", search, name="search"),
    path("user/", include("user.urls")),
    path("board/", include("board.urls")),
]
