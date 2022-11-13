from django.views import generic
from .models import Community, Comment, News, Column, Notice, Event
from .forms import CommuModelForm, NewsModelForm, ColumnModelForm
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import Http404
from django.core.paginator import Paginator


class CommunityListView(generic.ListView):
    template_name = "board/community_list.html"
    model = Community
    paginate_by = 40

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


def community_search(request):
    commu_hot_list = Community.objects.order_by("-like")[:5]
    commu_hot_list2 = Community.objects.order_by("-like")[5:10]
    if request.method == "POST":
        q = request.POST.get("q")
        community = Community.objects.filter(title__contains=q)
        paginator = Paginator(community, 40)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/community_search.html",
            {
                "q": q,
                "page_obj": page_obj,
                "commu_hot_list": commu_hot_list,
                "commu_hot_list2": commu_hot_list2,
            },
        )
    else:
        q = request.GET.get("q")
        community = Community.objects.filter(title__contains=q)
        paginator = Paginator(community, 40)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/community_search.html",
            {
                "q": q,
                "page_obj": page_obj,
                "commu_hot_list": commu_hot_list,
                "commu_hot_list2": commu_hot_list2,
            },
        )


class CommunityDetailView(generic.DetailView):
    template_name = "board/community_detail.html"
    model = Community
    context_object_name = "board"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


class CommunityCreateView(generic.CreateView):
    template_name = "board/community_form.html"
    form_class = CommuModelForm

    def get_success_url(self):
        return reverse_lazy("board:community_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
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

    if board.like_users.filter(id=request.user.id).exists():
        board.like_users.remove(request.user)
        message = "off"
        if request.user.is_authenticated:
            board.like -= 1
            board.save()
    elif not request.user.is_authenticated:
        message = "notlogin"
    else:
        board.like_users.add(request.user)
        message = "on"
        if request.user.is_authenticated:
            board.like += 1
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
        data = {
            "writer": request.POST.get("writer"),
            "content": request.POST.get("content"),
            "date": comment.date,
            "comment_id": comment.id,
            "comment_count": community.comment_set.count(),
            "img": request.user.image.url,
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


def news_search(request):
    if request.method == "POST":
        q = request.POST.get("q")
        news = News.objects.filter(title__contains=q)
        paginator = Paginator(news, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/news_search.html",
            {
                "q": q,
                "page_obj": page_obj,
            },
        )
    else:
        q = request.GET.get("q")
        news = News.objects.filter(title__contains=q)
        paginator = Paginator(news, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/news_search.html",
            {
                "q": q,
                "page_obj": page_obj,
            },
        )


class NewsDetailView(generic.DetailView):
    template_name = "board/news_detail.html"
    model = News
    context_object_name = "news"


class NewsCreateView(generic.CreateView):
    template_name = "board/news_form.html"
    form_class = NewsModelForm

    def get_success_url(self):
        return reverse_lazy("board:news_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
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


def column_search(request):
    if request.method == "POST":
        q = request.POST.get("q")
        column = Column.objects.filter(title__contains=q)
        paginator = Paginator(column, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/column_search.html",
            {
                "q": q,
                "page_obj": page_obj,
            },
        )
    else:
        q = request.GET.get("q")
        column = Column.objects.filter(title__contains=q)
        paginator = Paginator(column, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/column_search.html",
            {
                "q": q,
                "page_obj": page_obj,
            },
        )


class ColumnDetailView(generic.DetailView):
    template_name = "board/column_detail.html"
    model = Column
    context_object_name = "news"


class ColumnCreateView(generic.CreateView):
    template_name = "board/column_form.html"
    form_class = ColumnModelForm

    def get_success_url(self):
        return reverse_lazy("board:column_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
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


class EventListView(generic.ListView):
    queryset = Event.objects.order_by("-id")
    template_name = "board/event_list.html"
    paginate_by = 10


def event_search(request):
    if request.method == "POST":
        q = request.POST.get("q")
        event = Event.objects.filter(title__contains=q)
        paginator = Paginator(event, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/event_search.html",
            {
                "q": q,
                "page_obj": page_obj,
            },
        )
    else:
        q = request.GET.get("q")
        event = Event.objects.filter(title__contains=q)
        paginator = Paginator(event, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        return render(
            request,
            "board/event_search.html",
            {
                "q": q,
                "page_obj": page_obj,
            },
        )


class EventDetailView(generic.DetailView):
    template_name = "board/event_detail.html"
    model = Event
    context_object_name = "board"
