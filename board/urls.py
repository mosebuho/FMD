from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("community/", views.CommunityListView.as_view(), name="community_list"),
    path("community/search/",views.community_search,name="community_search"),
    path("community/<int:pk>/", views.CommunityDetailView.as_view(),name="community_detail"),
    path("community/create/",views.CommunityCreateView.as_view(),name="community_create"),
    path("community/<int:pk>/update/",views.CommunityUpdateView.as_view(),name="community_update"),
    path("community/<int:pk>/delete/", views.community_delete, name="community_delete"),
    path("like/", views.like, name="like"),
    path("<int:pk>/comment/create/", views.comment_create, name="comment_create"),
    path("comment/update/", views.comment_update, name="comment_update"),
    path("<int:pk>/comment/delete/", views.comment_delete, name="comment_delete"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/search/", views.news_search, name="news_search"),
    path("news/<int:pk>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/delete/", views.news_delete, name="news_delete"),
    path("news/<int:pk>/update/",views.NewsUpdateView.as_view(),name="news_update"),
    path("column/", views.ColumnListView.as_view(), name="column_list"),
    path("column/search/", views.column_search, name="column_search"),
    path("column/<int:pk>/", views.ColumnDetailView.as_view(), name="column_detail"),
    path("column/create/", views.ColumnCreateView.as_view(), name="column_create"),
    path("column/<int:pk>/delete/", views.column_delete, name="column_delete"),
    path("column/<int:pk>/update/",views.ColumnUpdateView.as_view(), name="column_update"),
    path("event/", views.EventListView.as_view(), name="event_list"),
    path("event/search/", views.event_search, name="event_search"),
    path("event/create/", views.EventCreateView.as_view(), name="event_create"),
    path("event/<int:pk>/update/", views.EventUpdateView.as_view(), name="event_update"),
    path("event/<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    path("notice/", views.NoticeListView.as_view(), name="notice"),
    path("notice/create/", views.NoticeCreateView.as_view(), name="notice_create"),
    path("notice/<int:pk>/update/", views.NoticeUpdateView.as_view(), name="notice_update"),
    path("notice/<int:pk>/delete/", views.notice_delete, name="notice_delete"),
    path("question/", views.question, name="question"),
    path("summernote/", views.summernote, name="summernote"),
]
