from user.models import User
from board.models import Event, Comment


def side_context(request):
    return {
        "events": Event.objects.order_by("-id")[:7],
        "ranking": User.objects.filter(verified=1)[:5],
        "comments": Comment.objects.order_by("-id")[:9],
    }
