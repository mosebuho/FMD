from user.models import User


def side_context(request):
    return {
        "ranking": User.objects.order_by("-point")[:5],
    }
