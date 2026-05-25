from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketAttachment,
)


class TicketAttachmentEntity(
    BaseEntity
):

    model = TicketAttachment

    entity = "ticket-attachments"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "ticket",

        "original_name",

        "mime_type",

        "size",

        "uploaded_by",

        "created_at",
    ]

    search_fields = [
        "original_name",
    ]

    filter_fields = [
        "ticket",
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
            "ticket_attachments.view",

        "view":
            "ticket_attachments.view",

        "create":
            "ticket_attachments.create",

        "edit":
            "ticket_attachments.edit",

        "delete":
            "ticket_attachments.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [

            "ticket",

            "field",

            "uploaded_by",
        ]