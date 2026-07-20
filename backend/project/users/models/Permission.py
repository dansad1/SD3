from django.db import models


class Permission(models.Model):

    code = models.CharField(
        "Код",
        max_length=255,
        unique=True,
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

    category = models.CharField(
        "Категория",
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "category",
            "code",
        ]

        verbose_name = "Разрешение"
        verbose_name_plural = "Разрешения"

    def __str__(self):

        return self.code
