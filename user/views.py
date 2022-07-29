from django.views import generic
from .forms import RegisterForm
from django.urls import reverse

class RegisterView(generic.CreateView):
    template_name = "user/register.html"
    form_class = RegisterForm
    def get_success_url(self):
        return reverse("user:login")