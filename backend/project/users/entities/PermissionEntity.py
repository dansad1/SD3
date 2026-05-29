
from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.users.models import Permission


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
        "id",
        "codename",
        "name",
    ]

    search_fields = [
        "codename",
        "name",
        "content_type__app_label",
    ]

    ordering = [
        "content_type__app_label",
        "codename",
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
                    f"{obj.content_type.app_label}."
                    f"{obj.codename}"
                ),
        }

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_name(
        self,
        obj,
    ):

        return (
            f"{obj.content_type.app_label}."
            f"{obj.codename}"
        )

    def represent_codename(
        self,
        obj,
    ):

        return obj.codename