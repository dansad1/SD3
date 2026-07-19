from backend.project.notifications.services.NotificationService import (
    NotificationService,
)


class TicketNotificationService:

    @classmethod
    def process(
        cls,
        *,
        ticket,
        created=False,
        changes=None,
        user=None,
    ):
        if hasattr(
            changes,
            "to_list",
        ):
            changes = changes.to_list()

        changes = changes or []

        print("=" * 80)
        print("TICKET NOTIFICATION PROCESS")
        print("ticket:", ticket.pk)
        print("created:", created)
        print("changes:", changes)
        print("=" * 80)

        context = {
            "ticket": ticket,
            "actor": user,
            "user": user,
            "changes": changes,
        }

        if created:
            print("TRIGGER: ticket.created")

            return NotificationService.trigger(
                "ticket.created",
                **context,
            )

        if not changes:
            print("NOTIFICATION SKIPPED: no changes")
            return None

        print("TRIGGER: ticket.changed")

        return NotificationService.trigger(
            "ticket.changed",
            **context,
        )