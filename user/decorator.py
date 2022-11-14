from django.shortcuts import redirect


def verified_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        else:
            if request.user.verified:
                return function(request, *args, **kwargs)
            else:
                return redirect("/")
    return wrap


def staff_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        else:
            if request.user.is_staff:
                return function(request, *args, **kwargs)
            else:
                return redirect("/")
    return wrap
