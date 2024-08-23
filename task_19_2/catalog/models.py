from django.db import models


class Contact(models.Model):
    name = models.CharField("Имя", max_length=30)
    phone = models.CharField("Номер телефона", max_length=12)
    message = models.TextField("Текст сообщения")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ("name",)

    def __str__(self):
        return self.name
