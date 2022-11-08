from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("check/", views.check, name="check"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", views.name_edit, name="name_edit"),
]
