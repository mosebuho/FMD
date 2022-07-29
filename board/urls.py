from django.urls import path
from .views import BoardlistView

app_name = "board"
urlpatterns = [
    path("", BoardlistView.as_view()),
]
