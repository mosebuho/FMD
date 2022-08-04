from django.views import generic
from .models import Community


class CommunitylistView(generic.ListView):
    template_name = "board/community.html"
    model = Community

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hot_list"] = Community.objects.order_by("-like")[0:5]
        context["hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context