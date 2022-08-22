from django.views import generic
from .models import Community
from .forms import CommuModelForm
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from FMD.views import HomeView

class CommunityListView(generic.ListView):
    template_name = "board/community_list.html"
    queryset = Community.objects.order_by("-id")
    paginate_by = 31
    context_object_name = "lists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


class CommunityDetailView(generic.DetailView):
    template_name = "board/community_detail.html"
    model = Community
    context_object_name = "detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context
    


class CommunityCreateView(generic.CreateView):
    template_name = "board/community_write.html"
    form_class = CommuModelForm
    success_url = "/board/community/"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 2
        self.request.user.save()
        return super().form_valid(form)


def like(request):
    detail_id = request.GET["detail_id"]
    detail = Community.objects.get(id=detail_id)
    writer = User.objects.get(id=detail.writer_id)

    if detail.like_users.filter(id=request.user.id).exists():
        detail.like_users.remove(request.user)
        message = "off"
        if request.user.is_authenticated:
            writer.point -= 1
            detail.like -= 1
            writer.save()
            detail.save()
    elif not request.user.is_authenticated:
        message = "notlogin"
    else:
        detail.like_users.add(request.user)
        message = "on"
        if request.user.is_authenticated:
            writer.point += 1
            detail.like += 1
            writer.save()
            detail.save()
    data = {"like": detail.like, "message": message}
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )
