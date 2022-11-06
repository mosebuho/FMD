from django.urls import path, include
from . import views

app_name = "user"
urlpatterns = [
    path("check/", views.check, name="check")
]
