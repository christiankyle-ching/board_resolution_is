from users.models import ROLE_ADMIN
from django.contrib.auth import get_user_model

_User = get_user_model()


def other_accounts(request):
    other_accounts = _User.objects.none()

    if request.user.is_authenticated:
        if request.user.role == ROLE_ADMIN:
            other_accounts = _User.objects.exclude(pk=request.user.pk)

    return {
        'other_accounts': other_accounts
    }
