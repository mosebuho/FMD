from django.views import generic
from board.models import Community


class HomeView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_list_free"] = Community.objects.filter(name="자유")[:14]
        context["commu_list_info"] = Community.objects.filter(name="정보")[:14]
        return context
