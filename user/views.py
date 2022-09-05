from django.views import generic
from .forms import RegisterForm, UserUpdateForm
from django.urls import reverse
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(generic.CreateView):
    template_name = "user/register.html"
    form_class = RegisterForm

    def get_success_url(self):
        return reverse("user:login")


class ProfileView(generic.TemplateView):
    template_name = "user/profile.html"
    model = User

    
class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/userupdate.html"

    def get_success_url(self):
        return reverse_lazy("user:profile", kwargs={"pk": self.object.pk})

