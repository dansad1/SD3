from django.db import transaction

from backend.project.tickets.services.TicketNotificationService import (
    TicketNotificationService,
)
from backend.project.tickets.services.TicketSLAService import (
    TicketSLAService,
)


class TicketAfterSaveService:

    @classmethod
    def process(
        cls,
        *,
        ctx,
    ):
        ticket = ctx.instance

        TicketSLAService.update_deadline(
            ticket,
        )

        created = (
            getattr(
                ctx,
                "mode",
                None,
            )
            == "create"
        )

        changes = getattr(
            ctx,
            "changes",
            None,
        )

        request = ctx.request
        user = getattr(
            request,
            "user",
            None,
        )

        transaction.on_commit(
            lambda: TicketNotificationService.process(
                ticket=ticket,
                created=created,
                changes=changes,
                user=user,
            )
        )