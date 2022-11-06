from django.views import generic
from .forms import RegisterForm, UserUpdateForm
from django.urls import reverse
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import JsonResponse


class RegisterView(generic.CreateView):
    template_name = "user/register.html"
    form_class = RegisterForm

    def get_success_url(self):
        return reverse("user:login")


class ProfileView(generic.DetailView):
    template_name = "user/profile.html"
    model = User
    context_object_name = "user"


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/userupdate.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.id != self.request.user.id:
            raise Http404("정보를 수정할 권한이 없습니다.")
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("user:profile", kwargs={"pk": self.object.pk})


def check(request):
    if request.GET.get("userid"):
        userid = request.GET.get("userid")
        try:
            user = User.objects.get(userid=userid)
        except:
            user = None
        if user is None:
            check = "pass"
        else:
            check = "fail"
        context = {"check": check}
        return JsonResponse(context)
    elif request.GET.get("name"):
        name = request.GET.get("name")
        try:
            user = User.objects.get(name=name)
        except:
            user = None
        if user is None:
            check = "pass"
        else:
            check = "fail"
        context = {"check": check}
        return JsonResponse(context)
    elif request.GET.get("email"):
        email = request.GET.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        if user is None:
            check = "pass"
        else:
            check = "fail"
        context = {"check": check}
        return JsonResponse(context)
