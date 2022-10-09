from django.views import generic
from .models import Community, Comment, News, Column, Notice, Event
from .forms import (
    CommuModelForm,
    NewsModelForm,
    ColumnModelForm,
    NoticeModelForm,
    EventModelForm,
)
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404
from user.decorator import *
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render


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


@method_decorator(lv1_required, name="dispatch")
class CommunityCreateView(generic.CreateView):
    template_name = "board/community_form.html"
    form_class = CommuModelForm

    def get_success_url(self):
        return reverse_lazy("board:community_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 2
        self.request.user.save()
        return super().form_valid(form)


class CommunityUpdateView(generic.UpdateView):
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
        return redirect("board:community_list")


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


@method_decorator(lv2_required, name="dispatch")
class NewsCreateView(generic.CreateView):
    template_name = "board/news_form.html"
    form_class = NewsModelForm

    def get_success_url(self):
        return reverse_lazy("board:news_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 5
        self.request.user.save()
        return super().form_valid(form)


def news_delete(request, pk):
    board = get_object_or_404(News, id=pk)
    if board.writer == request.user:
        board.delete()
        return redirect("board:news_list")
    else:
        return redirect("board:news_list")


class NewsUpdateView(generic.UpdateView):
    model = News
    form_class = NewsModelForm
    template_name = "board/news_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.writer != self.request.user:
            raise Http404("글을 수정할 권한이 없습니다.")
        return super(NewsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:news_detail", kwargs={"pk": self.object.pk})


class ColumnListView(generic.ListView):
    template_name = "board/column_list.html"
    model = Column
    paginate_by = 10
    context_object_name = "lists"


class ColumnDetailView(generic.DetailView):
    template_name = "board/column_detail.html"
    model = Column
    context_object_name = "news"


@method_decorator(lv2_required, name="dispatch")
class ColumnCreateView(generic.CreateView):
    template_name = "board/column_form.html"
    form_class = ColumnModelForm

    def get_success_url(self):
        return reverse_lazy("board:column_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 5
        self.request.user.save()
        return super().form_valid(form)


def column_delete(request, pk):
    board = get_object_or_404(Column, id=pk)
    if board.writer == request.user:
        board.delete()
        return redirect("board:column_list")
    else:
        return redirect("board:column_list")


class ColumnUpdateView(generic.UpdateView):
    model = Column
    form_class = ColumnModelForm
    template_name = "board/column_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.writer != self.request.user:
            raise Http404("글을 수정할 권한이 없습니다.")
        return super(ColumnUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:column_detail", kwargs={"pk": self.object.pk})


class NoticeListView(generic.ListView):
    model = Notice
    template_name = "board/notice_list.html"
    context_name = "notice_list"
    paginate_by = 33



@method_decorator(lv3_required, name="dispatch")
class NoticeCreateView(generic.CreateView):
    model = Notice
    form_class = NoticeModelForm
    template_name = "board/notice_form.html"
    success_url = "/board/notice/"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


@method_decorator(lv3_required, name="dispatch")
class NoticeUpdateView(generic.UpdateView):
    model = Notice
    form_class = NoticeModelForm
    template_name = "board/notice_form.html"
    success_url = "/board/notice/"


@lv3_required
def notice_delete(request, pk):
    board = get_object_or_404(Notice, id=pk)
    board.delete()
    return redirect("board:notice")


class EventListView(generic.ListView):
    model = Event
    template_name = "board/event_list.html"
    paginate_by = 10
    context_object_name = "events"


class EventDetailView(generic.DetailView):
    template_name = "board/event_detail.html"
    model = Event
    context_object_name = "board"


@method_decorator(lv3_required, name="dispatch")
class EventCreateView(generic.CreateView):
    model = Event
    template_name = "board/event_form.html"
    form_class = EventModelForm

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("board:event_detail", kwargs={"pk": self.object.pk})

@method_decorator(lv3_required, name="dispatch")
class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = "board/event_form.html"

    def get_success_url(self):
        return reverse_lazy("board:event_detail", kwargs={"pk": self.object.pk})


@lv3_required
def event_delete(request, pk):
    board = get_object_or_404(Event, id=pk)
    board.delete()
    return redirect("board:event_list")
