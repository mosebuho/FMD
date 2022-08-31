from django.urls import path
from .views import RegisterView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "user"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
]
