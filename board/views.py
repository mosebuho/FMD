from django.views import generic
from .models import Community, Comment, News
from .forms import CommuModelForm, NewsModelForm
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


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

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.writer != self.request.user:
            raise Http404("글을 수정할 권한이 없습니다.")
        return super(CommunityUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:community_detail", kwargs={"pk": self.object.pk})


def community_delete(request, pk):
    board = get_object_or_404(Community, id=pk)
    if board.writer == request.user:
        board.delete()
        return redirect("board:community_list")
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
    comment = Comment.objects.get(pk=comment_id)
    board = get_object_or_404(Community, id=pk)
    edit_comment = request.POST.get("edit_comment")
    if request.user == comment.writer:
        if edit_comment:
            comment.content = edit_comment
            comment.save()
            board.save()
    data = {
        "comment_id": comment_id,
        "content": comment.content,
        "edit_comment": edit_comment,
    }
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


def comment_delete(request, pk):
    board = get_object_or_404(Community, id=pk)
    comment_id = request.POST.get("comment_id")
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.writer:
        comment.delete()
        board.save()
        data = {
            "comment_id": comment_id,
            "comment_count": board.comment_set.count(),
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


class NewsListView(generic.ListView):
    template_name = "board/news_list.html"
    model = News
    paginate_by = 10
    context_object_name = "lists"


class NewsDetailView(generic.DetailView):
    template_name = "board/news_detail.html"
    model = News
    context_object_name = "news"


class NewsCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "board/news_form.html"
    form_class = NewsModelForm

    def get_success_url(self):
        return reverse_lazy("board:news_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 5
        self.request.user.save()
        return super().form_valid(form)
