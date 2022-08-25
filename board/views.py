from django.views import generic
from .models import Community, Comment
from .forms import CommuModelForm
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from django.shortcuts import get_object_or_404


class CommunityListView(generic.ListView):
    template_name = "board/community_list.html"
    model = Community
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
    context_object_name = "board"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


class CommunityCreateView(generic.CreateView):
    template_name = "board/community_form.html"
    form_class = CommuModelForm
    success_url = "/board/community/"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 2
        self.request.user.save()
        return super().form_valid(form)


class CommunityUpdateView(generic.UpdateView):
    model = Community
    form_class = CommuModelForm
    template_name = "board/community_form.html"
    success_url = "/board/community/"


def like(request):
    board_id = request.GET["board_id"]
    board = Community.objects.get(id=board_id)
    writer = User.objects.get(id=board.writer_id)

    if board.like_users.filter(id=request.user.id).exists():
        board.like_users.remove(request.user)
        message = "off"
        if request.user.is_authenticated:
            writer.point -= 1
            board.like -= 1
            writer.save()
            board.save()
    elif not request.user.is_authenticated:
        message = "notlogin"
    else:
        board.like_users.add(request.user)
        message = "on"
        if request.user.is_authenticated:
            writer.point += 1
            board.like += 1
            writer.save()
            board.save()
    data = {"like": board.like, "message": message}
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


def comment_create(request, pk):
    community = get_object_or_404(Community, id=pk)
    if request.POST.get("content"):
        comment = Comment.objects.create(
            community=community,
            content=request.POST.get("content"),
            writer=request.user,
        )
        community.save()
        request.user.point += 1
        request.user.save()
        data = {
            "writer": request.POST.get("writer"),
            "content": request.POST.get("content"),
            "date": comment.date,
            "comment_id": comment.id,
            "comment_count": community.comment_set.count(),
        }
        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
        )
