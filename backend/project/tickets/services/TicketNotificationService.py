

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

        changes = changes or {}

        context = {
            "ticket": ticket,
            "user": user,
            "changes": changes,
        }

        # =====================================================
        # CREATED
        # =====================================================

        if created:

            NotificationService.trigger(
                "ticket.created",
                **context,
            )

            return

        # =====================================================
        # CHANGED
        # =====================================================

        if not changes:
            return

        NotificationService.trigger(
            "ticket.changed",
            **context,
        )