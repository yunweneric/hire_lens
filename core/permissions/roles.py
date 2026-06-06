"""Role-based permission helpers."""

from functools import wraps

from django.contrib.auth.decorators import user_passes_test


def user_is_admin(user) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = getattr(user, "profile", None)
    return profile is not None and profile.role == "admin"


def user_is_recruiter(user) -> bool:
    if not user.is_authenticated:
        return False
    profile = getattr(user, "profile", None)
    return profile is not None and profile.role in ("admin", "recruiter")


class IsAdmin:
    """Callable for @user_passes_test."""

    def __call__(self, user):
        return user_is_admin(user)


class IsRecruiter:
    """Callable for @user_passes_test."""

    def __call__(self, user):
        return user_is_recruiter(user)


def admin_required(view_func):
    """Require authenticated admin or superuser."""

    @wraps(view_func)
    @user_passes_test(user_is_admin, login_url="accounts:login")
    def _wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped


def recruiter_required(view_func):
    """Require authenticated recruiter or admin."""

    @wraps(view_func)
    @user_passes_test(user_is_recruiter, login_url="accounts:login")
    def _wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped
