from collections import OrderedDict

from django.core.exceptions import (
    ValidationError
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.project.users.models import (
    UserRole,
    Permission,
)
from backend.project.users.services.UserRoleSchemaService import UserRoleSchemaService
from backend.project.users.services.UserRoleValidationService import UserRoleValidationService


class UserRoleEntity(BaseEntity):

    # =====================================================
    # CORE
    # =====================================================

    model = UserRole

    entity = "roles"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "code",
        "name",
        "is_active",
        "priority",
    ]

    search_fields = [
        "code",
        "name",
    ]

    filter_fields = [
        "is_active",
    ]

    ordering = [
        "name",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "roles.view",
        "view": "roles.view",
        "create": "roles.create",
        "edit": "roles.edit",
        "delete": "roles.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def apply_user_scope(
        self,
        request,
        qs,
    ):

        return qs

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,
            "label": obj.name,
            "code": obj.code,
        }

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_is_active(
        self,
        obj,
    ):

        return (
            "Активна"
            if obj.is_active
            else "Отключена"
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
            self,
            request,
            payload,
            instance=None,
    ):
        return (
            UserRoleValidationService
            .validate(
                payload=payload,
                instance=instance,
            )
        )
    # =====================================================
    # DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        if instance.users.exists():

            raise ValidationError({
                "detail": [
                    "Role has users"
                ]
            })

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
            self,
            request,
            schema,
            field=None,
    ):
        return (
            UserRoleSchemaService
            .customize(
                request=request,
                schema=schema,
                field=field,
            )
        )