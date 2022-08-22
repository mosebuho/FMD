from board.models import Community
from user.models import User


def default_context(request):
    return {
        "ranking": User.objects.order_by("-point")[:5],
    }
