from core.permissions import user_is_admin


def user_role(request):
    return {
        "is_admin": user_is_admin(request.user) if request.user.is_authenticated else False,
    }
