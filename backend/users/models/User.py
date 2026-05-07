from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from backend.users.models.managers.UserManager import UserManager


class User(
    AbstractBaseUser,
    PermissionsMixin,
):

    # =========================
    # AUTH
    # =========================

    login = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    password = models.CharField(
        max_length=255,
    )

    # =========================
    # ACCESS
    # =========================

    role = models.ForeignKey(
        "users.UserRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    # =========================
    # SYSTEM
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # =========================
    # DJANGO AUTH
    # =========================

    USERNAME_FIELD = "login"

    REQUIRED_FIELDS = []

    objects = UserManager()

    # =========================
    # STR
    # =========================

    def __str__(self):
        return self.login