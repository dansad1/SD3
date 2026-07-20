from django.conf import settings
from django.db import models

from backend.generic.models import TimeStampedModel


class Service(TimeStampedModel):

    # =====================================================
    # TREE
    # =====================================================

    parent = models.ForeignKey(
        "self",
        verbose_name="Родительский сервис",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    # =====================================================
    # BASE
    # =====================================================

    name = models.CharField(
        "Название",
        max_length=255,
    )

    code = models.CharField(
        "Код",
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        "Описание",
        blank=True,
    )

    # =====================================================
    # OWNER
    # =====================================================

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="owned_services",
    )

    # =====================================================
    # SCHEDULE
    # =====================================================

    schedule = models.ForeignKey(
        "services.WorkSchedule",
        verbose_name="График работы",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="services",
    )

    # =====================================================
    # ACCESS
    # =====================================================

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователи",
        blank=True,
        related_name="services",
    )

    companies = models.ManyToManyField(
        "companies.Company",
        verbose_name="Компании",
        blank=True,
        related_name="services",
    )

    roles = models.ManyToManyField(
        "users.UserRole",
        verbose_name="Роли",
        blank=True,
        related_name="services",
    )

    # =====================================================
    # TICKETS
    # =====================================================

    ticket_types = models.ManyToManyField(
        "tickets.TicketType",
        verbose_name="Типы заявок",
        blank=True,
        related_name="services",
    )

    ticket_categories = models.ManyToManyField(
        "tickets.TicketCategory",
        verbose_name="Категории заявок",
        blank=True,
        related_name="services",
    )

    # =====================================================
    # SYSTEM
    # =====================================================

    archived = models.BooleanField(
        "Архивирован",
        default=False,
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"

    def __str__(self):

        return self.get_full_path()

    def get_full_path(self):

        parts = [self.name]

        parent = self.parent

        while parent:

            parts.append(
                parent.name
            )

            parent = parent.parent

        return " / ".join(
            reversed(parts)
        )

    @property
    def has_children(self):

        return self.children.exists()
