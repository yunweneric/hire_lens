from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from features.accounts.forms import LoginForm


class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
