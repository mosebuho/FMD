from .models import User
from django.http import JsonResponse


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
