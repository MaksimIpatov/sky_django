from django.db import models

from users.models import User


class Contact(models.Model):
    name = models.CharField(
        "Имя",
        max_length=30,
    )
    phone = models.CharField(
        "Номер телефона",
        max_length=12,
    )
    message = models.TextField(
        "Текст сообщения",
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(
        "Наименование",
        max_length=60,
        unique=True,
    )
    description = models.TextField(
        "Описание",
    )
    image = models.ImageField(
        "Изображение",
        upload_to="products/%Y%m%d/",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.PositiveIntegerField(
        "Цена за покупку",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Дата последнего изменения",
        auto_now=True,
    )
    author = models.ForeignKey(
        User,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(
        "Признак публикации",
        default=True,
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("title",)
        permissions = [
            (
                "can_cancel_publication",
                "может отменять публикацию продукта",
            ),
            (
                "can_change_description",
                "может менять описание любого продукта",
            ),
            (
                "can_change_category",
                "может менять категорию любого продукта",
            ),
        ]

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        "Наименование",
        max_length=60,
        unique=True,
    )
    description = models.TextField(
        "Описание",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("title",)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(
        "Заголовок",
        max_length=60,
        unique=True,
    )
    slug = models.CharField(
        "SLUG",
        max_length=100,
        unique=True,
        blank=True,
    )
    preview = models.ImageField(
        "Превью",
        upload_to="previews/%Y%m/",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now=True,
    )
    is_published = models.BooleanField(
        "Признак публикации",
        default=True,
    )
    views = models.PositiveBigIntegerField(
        "Количество просмотров",
        default=0,
        blank=True,
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блог"
        ordering = (
            "-created_at",
            "is_published",
        )

    def __str__(self):
        return self.title


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="versions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Товар",
    )
    major = models.PositiveSmallIntegerField(
        "Номер версии",
        default=0,
        null=True,
        blank=True,
    )
    build = models.CharField(
        "Название версии",
        max_length=60,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        "Признак текущей версии",
        default=True,
    )

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = (
            "build",
            "product",
            "major",
        )

    def __str__(self):
        return self.build
