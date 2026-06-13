from django.conf import settings
from django.db import models


class Service(models.Model):

    # =====================================================
    # TREE
    # =====================================================

    parent = models.ForeignKey(

        "self",

        null=True,
        blank=True,

        on_delete=models.SET_NULL,

        related_name="children",
    )

    # =====================================================
    # BASE
    # =====================================================

    name = models.CharField(
        max_length=255,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    # =====================================================
    # OWNER
    # =====================================================

    owner = models.ForeignKey(

        settings.AUTH_USER_MODEL,

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

        blank=True,

        related_name="services",
    )

    companies = models.ManyToManyField(

        "companies.Company",

        blank=True,

        related_name="services",
    )

    roles = models.ManyToManyField(

        "users.UserRole",

        blank=True,

        related_name="services",
    )

    # =====================================================
    # TICKETS
    # =====================================================

    ticket_types = models.ManyToManyField(

        "tickets.TicketType",

        blank=True,

        related_name="services",
    )

    ticket_categories = models.ManyToManyField(

        "tickets.TicketCategory",

        blank=True,

        related_name="services",
    )

    # =====================================================
    # SYSTEM
    # =====================================================

    archived = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:

        ordering = [
            "name",
        ]

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