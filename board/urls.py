from django.urls import path
from .views import BoardlistView

app_name = "board"
urlpatterns = [
    path("community/", BoardlistView.as_view(), name="community")
]
