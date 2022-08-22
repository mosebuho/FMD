from django.views import generic
from .models import Community
from .forms import CommuModelForm, CommentModelForm
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from user.models import User
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse


class CommunityListView(generic.ListView):
    template_name = "board/community_list.html"
    queryset = Community.objects.order_by("-id")
    paginate_by = 31
    context_object_name = "lists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        return context


class CommunityDetailView(generic.DetailView, FormMixin):
    template_name = "board/community_detail.html"
    model = Community
    form_class = CommentModelForm
    context_object_name = "board"

    def get_success_url(self):
        return reverse("board:community_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commu_hot_list"] = Community.objects.order_by("-like")[0:5]
        context["commu_hot_list2"] = Community.objects.order_by("-like")[5:10]
        context["comments"] = self.object.comment_set.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.community = get_object_or_404(Community, pk=self.object.pk)
        comment.writer = self.request.user
        comment.save()
        return super().form_valid(form)


class CommunityCreateView(generic.CreateView):
    template_name = "board/community_create.html"
    form_class = CommuModelForm
    success_url = "/board/community/"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        self.request.user.point += 2
        self.request.user.save()
        return super().form_valid(form)


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
