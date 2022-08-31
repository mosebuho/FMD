from django.views import generic
from .forms import RegisterForm
from django.urls import reverse
from .models import User
from django.shortcuts import get_object_or_404, render


class RegisterView(generic.CreateView):
    template_name = "user/register.html"
    form_class = RegisterForm

    def get_success_url(self):
        return reverse("user:login")


class ProfileView(generic.TemplateView):
    template_name = "user/profile.html"
    model = User
