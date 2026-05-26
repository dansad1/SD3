from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from backend.project.users.managers import (
    UserManager
)


class User(
    AbstractBaseUser,
    PermissionsMixin,
):

    # =====================================================
    # AUTH
    # =====================================================

    login = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    # =====================================================
    # ACCESS
    # =====================================================

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

    # =====================================================
    # DYNAMIC
    # =====================================================

    fieldset = models.ForeignKey(
        "users.UserFieldSet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    # =====================================================
    # SYSTEM
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # =====================================================
    # DJANGO AUTH
    # =====================================================

    USERNAME_FIELD = "login"

    REQUIRED_FIELDS = []

    objects = UserManager()

    # =====================================================
    # STR
    # =====================================================

    def __str__(self):

        return (
            self.get_value("full_name")
            or self.login
        )

    # =====================================================
    # DYNAMIC VALUES
    # =====================================================

    def get_dynamic_map(self):

        if hasattr(
            self,
            "_dynamic_map",
        ):
            return self._dynamic_map

        values = {}

        dynamic_values = (
            self.dynamic_values
            .select_related("field")
            .all()
        )

        for item in dynamic_values:

            if not item.field_id:
                continue

            values[
                item.field.name
            ] = item.value

        self._dynamic_map = values

        return values

    def get_value(
        self,
        field_name,
    ):

        # =============================================
        # STATIC
        # =============================================

        if hasattr(
            self,
            field_name,
        ):

            return getattr(
                self,
                field_name,
            )

        # =============================================
        # DYNAMIC
        # =============================================

        return (
            self.get_dynamic_map()
            .get(field_name)
        )