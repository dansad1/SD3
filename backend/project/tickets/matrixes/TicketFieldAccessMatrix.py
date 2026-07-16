from backend.project.audit.utils.BaseFieldAccessMatrix import BaseFieldAccessMatrix
from backend.project.tickets.models import (
    TicketField,
    TicketFieldAccess,
)


class TicketFieldAccessMatrix(
    BaseFieldAccessMatrix,
):

    field_model = TicketField

    access_model = TicketFieldAccess

    role_order = "name"

    class Meta:

        code = "ticket-field.access"

        capabilities = {
            "view": "ticket_fields.edit",
            "edit": "ticket_fields.edit",
        }