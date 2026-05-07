from django.core.exceptions import (
    ValidationError
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.users.models import (
    UserRole
)


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
        "priority",
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

        errors = {}

        # -------------------------------------------------
        # CODE
        # -------------------------------------------------

        code = payload.get(
            "code"
        )

        if code:

            reserved = {
                "root",
                "system",
                "superadmin",
            }

            if (
                code.lower()
                in reserved
            ):

                errors["code"] = [
                    "Reserved role code"
                ]

        # -------------------------------------------------
        # PRIORITY
        # -------------------------------------------------

        priority = payload.get(
            "priority"
        )

        if priority is not None:

            if priority < 0:

                errors["priority"] = [
                    "Priority must be >= 0"
                ]

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if errors:

            raise ValidationError(
                errors
            )

        return payload

    # =====================================================
    # DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        # нельзя удалить роль,
        # если есть пользователи

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

        # priority

        if schema["name"] == "priority":

            schema["min"] = 0

        # code

        if schema["name"] == "code":

            schema["autocomplete"] = False

        return schema