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

        print("=" * 80)
        print("TICKET AFTER SAVE")
        print("ticket:", ticket.pk)
        print("mode:", getattr(ctx, "mode", None))
        print("created:", created)
        print("changes:", changes)
        print("=" * 80)

        TicketSLAService.update_deadline(
            ticket,
        )

        def notify():
            print("=" * 80)
            print("TICKET NOTIFICATION ON COMMIT")
            print("ticket:", ticket.pk)
            print("=" * 80)

            TicketNotificationService.process(
                ticket=ticket,
                created=created,
                changes=changes,
                user=getattr(
                    ctx.request,
                    "user",
                    None,
                ),
            )

        transaction.on_commit(
            notify
        )