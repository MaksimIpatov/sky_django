from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import countries


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(
        "Электронная почта",
        unique=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Фото профиля",
        blank=True,
        null=True,
    )
    phone = models.CharField(
        "Номер телефона",
        unique=True,
        max_length=12,
        blank=True,
        null=True,
    )
    country = models.CharField(
        "Страна",
        choices=countries,
        blank=True,
        null=True,
    )
    token = models.CharField(
        "Токен активации",
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)

    def __str__(self):
        return self.email
