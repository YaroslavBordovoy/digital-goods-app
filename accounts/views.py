from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import RegisterForm
from accounts.services.email_service import EmailService
from accounts.services.token_service import account_activation_token

User = get_user_model()


def register(request: HttpRequest):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            email_service = EmailService()
            email_service.send_activation_email(
                username=user.username,
                domain=domain,
                uid=uid,
                to_email=user.email,
                token=token,
            )

            messages.info(request, "Please confirm your activation")

            return redirect("accounts:login")

    return render(request, "registration/register.html", {"form": form})


def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user.is_active:
        return HttpResponse("Your account is already activated")

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        if user.role == "SL":
            permissions = Permission.objects.filter(
                content_type__model__in=["category", "product"],
                content_type__app_label="digital_store",
            )
            user.user_permissions.add(*permissions)

        user.save()

        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")
