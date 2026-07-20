from django.db import models


class BaseFieldSet(models.Model):

    code = models.SlugField(
        "Код",
        max_length=100,
    )

    name = models.CharField(
        "Название",
        max_length=255,
    )

    description = models.TextField(
        "Описание",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        "Активен",
        default=True,
    )

    is_default = models.BooleanField(
        "Используется по умолчанию",
        default=False,
    )

    order = models.IntegerField(
        "Порядок",
        default=0,
    )

    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        "Обновлено",
        auto_now=True,
        editable=False,
    )

    class Meta:

        abstract = True
