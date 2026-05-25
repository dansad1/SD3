from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketComment,
)


class TicketCommentEntity(
    BaseEntity
):

    model = TicketComment

    entity = "ticket-comments"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "ticket",

        "author",

        "hide_from_client",

        "created_at",
    ]

    search_fields = [
        "text",
    ]

    filter_fields = [
        "ticket",
        "author",
        "hide_from_client",
    ]

    ordering = [
        "created_at",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "ticket_comments.view",

        "view":
            "ticket_comments.view",

        "create":
            "ticket_comments.create",

        "edit":
            "ticket_comments.edit",

        "delete":
            "ticket_comments.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "ticket",
            "author",
        ]