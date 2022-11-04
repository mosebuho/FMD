from user.models import User
from board.models import Event


def side_context(request):
    return {
        "ranking": User.objects.order_by("-point")[:5],
        "events": Event.objects.order_by("-id")[:10],
    }
