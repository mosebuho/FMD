from django.shortcuts import redirect


def lv1_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/user/login/")
        else:
            if request.user.level >= 1:
                return function(request, *args, **kwargs)
            else:
                return redirect("/")
    return wrap


def lv2_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/user/login/")
        else:
            if request.user.level >= 2:
                return function(request, *args, **kwargs)
            else:
                return redirect("/")
    return wrap