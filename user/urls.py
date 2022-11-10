from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("check/", views.check, name="check"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("edit/name/<int:pk>/", views.name_edit, name="name_edit"),
    path("edit/image/<int:pk>/", views.image_edit, name="image_edit"),
    path("quit/", views.quit, name="quit"),
]
