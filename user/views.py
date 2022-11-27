from .models import User
from django.http import JsonResponse
from django.views import generic
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def check(request):
    if request.GET.get("username"):
        username = request.GET.get("username")
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user is None:
            check = "pass"
        else:
            check = "fail"
        context = {"check": check}
        return JsonResponse(context)
    elif request.GET.get("nickname"):
        nickname = request.GET.get("nickname")
        try:
            user = User.objects.get(nickname=nickname)
        except:
            user = None
        if user is None:
            check = "pass"
        else:
            check = "fail"
        context = {"check": check}
        return JsonResponse(context)
    elif request.GET.get("email"):
        email = request.GET.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        if user is None:
            check = "pass"
        else:
            check = "fail"
        context = {"check": check}
        return JsonResponse(context)


class ProfileView(generic.DetailView):
    template_name = "account/profile.html"
    model = User
    context_object_name = "user"


def name_edit(request, pk):
    target = User.objects.get(pk=pk)
    edit_name = request.POST.get("edit_name")
    if request.user.id == target.id:
        if target.nchanged == True:
            target.nickname = edit_name
            target.n_changed = datetime.datetime.now()
            target.save()
            data = {
                "user_id": request.user.id,
                "edit_name": edit_name,
            }
        return JsonResponse(data)


def image_edit(request, pk):
    target = User.objects.get(pk=pk)
    edit_image = request.FILES.get("image")
    if request.user.id == target.id:
        target.image = edit_image
        target.save()
        url = target.image.url
        data = {"url": url}
    return JsonResponse(data)


def quit(request):
    if request.method == "GET":
        return render(request, "account/quit.html")
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("/")
