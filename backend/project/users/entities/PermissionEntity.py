from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.users.models import (
    Permission,
)


class PermissionEntity(
    BaseEntity
):

    # =====================================================
    # CORE
    # =====================================================

    model = Permission

    entity = "permissions"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "category",
        "code",
        "name",
    ]

    search_fields = [
        "code",
        "name",
        "description",
        "category",
    ]

    ordering = [
        "category",
        "code",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "roles.view",
        "view": "roles.view",
    }

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {

            "value":
                obj.pk,

            "label":
                (
                    obj.name
                    or obj.code
                ),

            "code":
                obj.code,

            "category":
                obj.category,

            "description":
                obj.description,
        }

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_name(
        self,
        obj,
    ):

        return (
            obj.name
            or obj.code
        )

    def represent_code(
        self,
        obj,
    ):

        return obj.code

    def represent_category(
        self,
        obj,
    ):

        return (
            obj.category
            or ""
        )