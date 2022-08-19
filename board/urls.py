from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("community/", views.CommunityListView.as_view(), name="community_list"),
    path(
        "community/<int:pk>/",
        views.CommunityDetailView.as_view(),
        name="community_detail",
    ),
    path(
        "community/write/", views.CommunityCreateView.as_view(), name="community_create"
    ),
    path("like/", views.like, name="like"),
]
