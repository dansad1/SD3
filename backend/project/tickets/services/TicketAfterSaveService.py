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

        # SLA

        TicketSLAService(
            ticket,
        ).recalculate()

        # Notifications

        transaction.on_commit(

            lambda: TicketNotificationService.process(

                ticket=ticket,

                created=getattr(
                    ctx,
                    "created",
                    False,
                ),

                changes=getattr(
                    ctx,
                    "changes",
                    {},
                ),

                user=ctx.request.user,

            )

        )