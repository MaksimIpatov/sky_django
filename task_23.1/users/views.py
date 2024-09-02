import secrets

from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import ResetPasswordForm, UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Подтвердите почту {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserResetPasswordView(PasswordResetView):
    form_class = ResetPasswordForm
    template_name = "users/reset_password.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = get_object_or_404(
            User,
            email=form.cleaned_data["email"],
        )
        if user:
            password = User.objects.make_random_password(length=12)
            user.set_password(password)
            user.save()
            send_mail(
                subject="Сброс пароля",
                message=f"Ваш новый пароль {password}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        return redirect(reverse("users:login"))


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
