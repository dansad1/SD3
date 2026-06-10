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

        priority = payload.get(
            "priority"
        )

        if priority is not None:

            if priority < 0:

                errors["priority"] = [
                    "Priority must be >= 0"
                ]

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
            field,
            schema,
            request=None,
            obj=None,
    ):

        if field.name != "permissions":
            return schema

        groups = OrderedDict()

        permissions = (
            Permission.objects
            .all()
            .order_by(
                "category",
                "code",
            )
        )

        for permission in permissions:

            category = (
                    permission.category
                    or "Общее"
            )

            if category not in groups:
                groups[category] = {

                    "name":
                        category,

                    "permissions":
                        [],
                }

            groups[category][
                "permissions"
            ].append({

                "id":
                    permission.pk,

                "value":
                    permission.pk,

                "code":
                    permission.code,

                "label":
                    (
                            permission.name
                            or permission.code
                    ),

                "description":
                    permission.description,
            })

        schema.update({

            "widget":
                "permission_editor",

            "groups":
                list(
                    groups.values()
                ),

        })

        return schema