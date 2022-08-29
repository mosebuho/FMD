from django.views import generic
from .models import Community, Comment
from .forms import CommuModelForm
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin


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


class CommunityDetailView(generic.DetailView, MultipleObjectMixin):
    template_name = "board/community_detail.html"
    model = Community
    context_object_name = "board"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(community=self.get_object())
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


class CommunityCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "board/community_form.html"
    form_class = CommuModelForm

    def get_success_url(self):
        return reverse_lazy("board:community_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 2
        self.request.user.save()
        return super().form_valid(form)


class CommunityUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Community
    form_class = CommuModelForm
    template_name = "board/community_form.html"

    def get_success_url(self):
        return reverse_lazy("board:community_detail", kwargs={"pk": self.object.pk})


def community_delete(request, pk):
    board = get_object_or_404(Community, id=pk)
    if board.writer == request.user:
        board.delete()
        return redirect("/")
    else:
        return redirect(f"/board/detail/{pk}/")


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
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


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
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


def comment_update(request, pk):
    comment_id = request.POST.get("comment_id")
    target_comment = Comment.objects.get(pk=comment_id)
    board = get_object_or_404(Community, id=pk)
    edit_comment = request.POST.get("edit_comment")
    if request.user == target_comment.writer:
        if edit_comment:
            target_comment.content = edit_comment
            target_comment.save()
            board.save()
    data = {
        "comment_id": comment_id,
        "content": target_comment.content,
        "edit_comment": edit_comment,
    }
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


def comment_delete(request, pk):
    board = get_object_or_404(Community, id=pk)
    comment_id = request.POST.get("comment_id")
    target_comment = Comment.objects.get(pk=comment_id)
    if request.user == target_comment.writer:
        target_comment.delete()
        board.save()
        data = {
            "comment_id": comment_id,
            "comment_count": board.comment_set.count(),
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))
