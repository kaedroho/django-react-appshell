import hashlib

from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.urls import reverse

from appshell.decorators import appshell_enable
from appshell.response import AppShellCloseModalResponse, AppShellResponse

from .forms import UserChangeForm


@login_required
@appshell_enable
def profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            # If the form is opened in a modal, close it
            if request.META.get("HTTP_X_SHELL_MODE", "browser") == "modal":
                return AppShellCloseModalResponse()
    else:
        form = UserChangeForm(instance=request.user)

    return AppShellResponse(
        request,
        "user-profile",
        {
            "user": {
                "displayName": request.user.get_full_name(),
                "avatarUrl": "https://www.gravatar.com/avatar/{}?s=128&d=identicon".format(
                    hashlib.md5(
                        request.user.email.lower().strip().encode("utf-8")
                    ).hexdigest()
                ),
            },
            "csrfToken": get_token(request),
            "form": form,
            "actionUrl": reverse("user_profile"),
        },
        supported_modes=["modal"],
    )
