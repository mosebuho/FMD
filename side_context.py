from user.models import User
from board.models import Event


def side_context(request):
    return {
        "events": Event.objects.order_by("-id")[:7],
    }
