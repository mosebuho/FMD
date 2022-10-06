from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("community/", views.CommunityListView.as_view(), name="community_list"),
    path("community/<int:pk>/", views.CommunityDetailView.as_view(),name="community_detail"),
    path("community/create/",views.CommunityCreateView.as_view(),name="community_create"),
    path("community/update/<int:pk>/",views.CommunityUpdateView.as_view(),name="community_update"),
    path("community/delete/<int:pk>/", views.community_delete, name="community_delete"),
    path("like/", views.like, name="like"),
    path("<int:pk>/comment/create/", views.comment_create, name="comment_create"),
    path("<int:pk>/comment/update/", views.comment_update, name="comment_update"),
    path("<int:pk>/comment/delete/", views.comment_delete, name="comment_delete"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/<int:pk>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/delete/<int:pk>/", views.news_delete, name="news_delete"),
    path("news/update/<int:pk>/",views.NewsUpdateView.as_view(),name="news_update"),
    path("column/", views.ColumnListView.as_view(), name="column_list"),
    path("column/<int:pk>/", views.ColumnDetailView.as_view(), name="column_detail"),
    path("column/create/", views.ColumnCreateView.as_view(), name="column_create"),
    path("column/delete/<int:pk>/", views.column_delete, name="column_delete"),
    path("column/update/<int:pk>/",views.ColumnUpdateView.as_view(), name="column_update"),
    path("event/", views.calendar, name="event"),
    path("notice/", views.NoticeListView.as_view(), name="notice"),
    path("notice/create/", views.NoticeCreateView.as_view(), name="notice_create"),
    path("notice/update/<int:pk>/", views.NoticeUpdateView.as_view(), name="notice_update"),
    path("notice/delete/<int:pk>/", views.notice_delete, name="notice_delete"),
]
