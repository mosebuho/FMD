from django.urls import path
from .views import CommunitylistView

app_name = "board"
urlpatterns = [
    path("community/", CommunitylistView.as_view(), name="community")
]
