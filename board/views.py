from django.views import generic
from .models import *
from .forms import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import Http404
from django.core.paginator import Paginator
from user.decorator import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
        comment_set = self.get_comment_set()
        context["commentset"] = comment_set
        context["page_obj"] = comment_set
        return context

    def get_comment_set(self):
        queryset = self.object.comment_set.order_by("-date")
        paginator = Paginator(queryset, 25)
        page = self.request.GET.get("page")
        board_comments = paginator.get_page(page)
        return board_comments


@method_decorator(login_required, name="dispatch")
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
    if request.user.is_authenticated:
        if board.like_users.filter(id=request.user.id).exists():
            board.like_users.remove(request.user)
            board.like -= 1
            board.save()
            data = {"like": board.like, "message": "off"}
        else:
            board.like_users.add(request.user)
            board.like += 1
            board.save()
            data = {"like": board.like, "message": "on"}
        return JsonResponse(data)


def comment_create(request, pk):
    community = get_object_or_404(Community, id=pk)
    if request.user.is_authenticated:
        if request.POST.get("content"):
            if request.POST.get("parents_id"):
                parents_id = request.POST.get("parents_id")
                parents = Comment.objects.get(pk=parents_id)
                comment = Comment.objects.create(
                    community=community,
                    content=request.POST.get("content"),
                    writer=request.user,
                    parents_id=parents.id,
                )
                comment.save()
            else:
                comment = Comment.objects.create(
                    community=community,
                    content=request.POST.get("content"),
                    writer=request.user,
                )
                comment.save()
        data = {
            "writer": request.POST.get("writer"),
            "content": request.POST.get("content"),
            "date_str": comment.date_str,
            "comment_id": comment.id,
            "comment_count": community.comment_set.count(),
            "img": request.user.image.url,
        }
        return JsonResponse(data)


def comment_update(request):
    comment_id = request.POST.get("comment_id")
    comment = Comment.objects.get(pk=comment_id)
    edit_comment = request.POST.get("edit_comment")
    if request.user == comment.writer:
        if edit_comment:
            comment.content = edit_comment
            comment.save()
        data = {
            "comment_id": comment_id,
            "content": comment.content,
        }
        return JsonResponse(data)


def comment_delete(request, pk):
    community = get_object_or_404(Community, id=pk)
    comment_id = request.POST.get("comment_id")
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.writer:
        comment.delete()
        data = {
            "comment_id": comment_id,
            "comment_count": community.comment_set.count(),
        }
        return JsonResponse(data)


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


@method_decorator(verified_required, name="dispatch")
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


@method_decorator(verified_required, name="dispatch")
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


@method_decorator(staff_required, name="dispatch")
class NoticeCreateView(generic.CreateView):
    model = Notice
    form_class = NoticeModelForm
    template_name = "board/notice_form.html"
    success_url = "/board/notice/"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


class NoticeUpdateView(generic.UpdateView):
    model = Notice
    form_class = NoticeModelForm
    template_name = "board/notice_form.html"
    success_url = "/board/notice/"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.writer != self.request.user:
            raise Http404("글을 수정할 권한이 없습니다.")
        return super(NoticeUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:event_detail", kwargs={"pk": self.object.pk})


def notice_delete(request, pk):
    board = get_object_or_404(Notice, id=pk)
    if board.writer == request.user:
        board.delete()
    return redirect("board:notice")


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


@method_decorator(staff_required, name="dispatch")
class EventCreateView(generic.CreateView):
    model = Event
    template_name = "board/event_form.html"
    form_class = EventModelForm

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("board:event_detail", kwargs={"pk": self.object.pk})


class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = "board/event_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.writer != self.request.user:
            raise Http404("글을 수정할 권한이 없습니다.")
        return super(EventUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:event_detail", kwargs={"pk": self.object.pk})


def event_delete(request, pk):
    board = get_object_or_404(Event, id=pk)
    if board.writer == request.user:
        board.delete()
    return redirect("board:event_list")


@csrf_exempt
def summernote(request):
    f2 = request.FILES.get("file")
    image = Image(image=f2)
    image.save()
    data = {"url": image.image.url}
    return JsonResponse(data)
