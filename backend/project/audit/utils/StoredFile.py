from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.generic.models import StoredFile


class StoredFileEntity(
    BaseEntity,
):

    model = StoredFile

    entity = "files"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "original_name",
        "mime_type",
        "size",
        "uploaded_by",
        "created_at",
    ]

    search_fields = [
        "original_name",
        "mime_type",
    ]

    filter_fields = [
        "uploaded_by",
    ]

    ordering = [
        "-created_at",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "files.view",

        "view":
            "files.view",

        "create":
            "files.upload",

        "edit":
            "files.edit",

        "delete":
            "files.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):

        return [
            "uploaded_by",
        ]

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,
            "label": obj.original_name,
        }