from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from backend.generic.models.DynamicModelMixin import (
    DynamicModelMixin,
)
from backend.project.users.managers import (
    UserManager,
)


class User(
    DynamicModelMixin,
    AbstractBaseUser,
    PermissionsMixin,
):

    # =====================================================
    # AUTH
    # =====================================================

    login = models.CharField(
        "Логин",
        max_length=255,
        unique=True,
        db_index=True,
    )

    # =====================================================
    # ACCESS
    # =====================================================

    role = models.ForeignKey(
        "users.UserRole",
        verbose_name="Роль",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    is_active = models.BooleanField(
        "Активен",
        default=True,
    )

    is_staff = models.BooleanField(
        "Сотрудник",
        default=False,
    )

    # =====================================================
    # DYNAMIC
    # =====================================================

    fieldset = models.ForeignKey(
        "users.UserFieldSet",
        verbose_name="Набор полей",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    # =====================================================
    # AUTH
    # =====================================================

    USERNAME_FIELD = "login"

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # =====================================================
    # STRING
    # =====================================================

    def __str__(
        self,
    ):
        return (
            self.get_value(
                "full_name",
            )
            or self.login
        )

    # =====================================================
    # VALUE
    # =====================================================

    def set_value(
        self,
        field_name,
        value,
    ):

        field = (
            self.fieldset.fields
            .filter(
                name=field_name,
            )
            .first()
        )

        if field is None:
            raise ValueError(
                f"Unknown field: {field_name}"
            )

        field.set_value(
            self,
            value,
        )

        self.invalidate_dynamic_cache()
