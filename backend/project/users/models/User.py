from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.contenttypes.fields import (
    GenericRelation,
)
from django.db import models

from backend.generic.models import (
    DynamicValue,
)
from backend.project.users.managers import (
    UserManager,
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    dynamic_values = GenericRelation(
        DynamicValue,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="user",
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
            self.get_value(
                "full_name"
            )
            or self.login
        )

    # =====================================================
    # DYNAMIC VALUES
    # =====================================================

    def get_dynamic_map(
        self,
    ):

        if hasattr(
            self,
            "_dynamic_map",
        ):
            return self._dynamic_map

        values = {}

        for item in self.dynamic_values.all():

            values[
                item.field_name
            ] = item.value

        self._dynamic_map = values

        return values

    # =====================================================
    # VALUE
    # =====================================================

    def get_value(
        self,
        field_name,
    ):

        if hasattr(
            self,
            field_name,
        ):
            return getattr(
                self,
                field_name,
            )

        return (
            self.get_dynamic_map()
            .get(field_name)
        )