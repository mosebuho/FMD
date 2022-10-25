from django.shortcuts import render
from django.views import generic
from board.models import Community, News, Column, Event


class HomeView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_new"] = Community.objects.all()[:16]
        context["commu_hot"] = Community.objects.all().order_by("-like")[:16]
        context["news_list"] = News.objects.order_by("-id")[:3]
        context["column_list"] = Column.objects.order_by("-id")[:6]
        return context


def search(request):
    if request.method == "POST":
        q = request.POST.get("q")
        community = Community.objects.filter(title__icontains=q)
        news = News.objects.filter(title__icontains=q)
        column = Column.objects.filter(title__icontains=q)
        event = Event.objects.filter(title__icontains=q)
        return render(
            request,
            "home/search.html",
            {
                "q": q,
                "community": community,
                "news": news,
                "column": column,
                "event": event,
            },
        )
    else:
        q = request.GET.get("q")
        community = Community.filter(title__icontains=q)
        news = News.filter(title__icontains=q)
        column = Column.filter(title__icontains=q)
        event = Event.filter(title__icontains=q)
        return render(
            request,
            "home/search.html",
            {
                "q": q,
                "community": community,
                "news": news,
                "column": column,
                "event": event,
            },
        )
