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
        actor=None,
    ):
        if hasattr(
            changes,
            "to_list",
        ):
            changes = changes.to_list()

        changes = changes or []

        context = {
            "ticket": ticket,
            "actor": actor,
            "changes": changes,
            "ticket_name": ticket.get_value(
                "name",
            ),
            "ticket_status": ticket.get_value(
                "status",
            ),
            "ticket_requester": ticket.get_value(
                "requester",
            ),
        }

        if created:
            return NotificationService.trigger(
                "ticket.created",
                **context,
            )

        if not changes:
            return None

        return NotificationService.trigger(
            "ticket.changed",
            **context,
        )