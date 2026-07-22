import logging

from django.db import transaction

from backend.project.tickets.models import (
    Ticket,
)
from backend.project.tickets.services.TicketNotificationService import (
    TicketNotificationService,
)
from backend.project.tickets.services.TicketSLAService import (
    TicketSLAService,
)

logger = logging.getLogger(
    __name__,
)


class TicketAfterSaveService:

    @classmethod
    def process(
        cls,
        *,
        ctx,
    ):
        ticket = ctx.instance
        ticket_id = ticket.pk

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

        if hasattr(
            changes,
            "to_list",
        ):
            changes = changes.to_list()

        changes = changes or []

        actor = getattr(
            ctx.request,
            "user",
            None,
        )

        TicketSLAService.update_deadline(
            ticket,
        )

        def notify():
            try:
                fresh_ticket = (
                    Ticket.objects
                    .select_related(
                        "type",
                    )
                    .prefetch_related(
                        "dynamic_values",
                        "dynamic_values__field",
                    )
                    .get(
                        pk=ticket_id,
                    )
                )

                TicketNotificationService.process(
                    ticket=fresh_ticket,
                    created=created,
                    changes=changes,
                    actor=actor,
                )
            except Ticket.DoesNotExist:
                logger.warning(
                    "Ticket notification skipped: "
                    "ticket=%s not found",
                    ticket_id,
                )
            except Exception:
                logger.exception(
                    "Ticket notification failed: "
                    "ticket=%s",
                    ticket_id,
                )

        transaction.on_commit(
            notify,
        )

        return ctx