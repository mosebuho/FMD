from django.views import generic
from .models import Community
from .forms import CommuModelForm
from user.models import User

class CommunityListView(generic.ListView):
    template_name = "board/community_list.html"
    queryset = Community.objects.order_by("-id")
    paginate_by = 30
    context_object_name = "commulist"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


class CommunityDetailView(generic.DetailView):
    template_name = "board/community_detail.html"
    model = Community
    context_object_name = "commudetail"

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