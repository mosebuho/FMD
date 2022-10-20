from django.shortcuts import render
from django.views import generic
from board.models import Community, News, Column, Event


class HomeView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_free_new"] = Community.objects.filter(name="자유")[:14]
        context["commu_info_new"] = Community.objects.filter(name="정보")[:14]
        context["commu_free_hot"] = Community.objects.filter(name="자유").order_by(
            "-like"
        )[:14]
        context["commu_info_hot"] = Community.objects.filter(name="정보").order_by(
            "-like"
        )[:14]
        context["news_list"] = News.objects.order_by("-id")[:3]
        context["column_list"] = Column.objects.order_by("-id")[:6]
        return context


def search(request):
    community = Community.objects.all().order_by("-id")
    news = News.objects.all().order_by("-id")
    column = Column.objects.all().order_by("-id")
    event = Event.objects.all().order_by("-id")

    q = request.POST.get("q", "")
    context = {"q": q}

    if q:
        community = community.filter(title__icontains=q)
        news = news.filter(title__icontains=q)
        column = column.filter(title__icontains=q)
        event = event.filter(title__icontains=q)
        context = {
            "community": community,
            "news": news,
            "column": column,
            "event": event,
        }
    return render(request, "home/search.html", context)
