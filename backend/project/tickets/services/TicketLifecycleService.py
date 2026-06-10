# backend/project/tickets/services/TicketLifecycleService.py
from backend.project.notifications.services.NotificationService import NotificationService


class TicketLifecycleService:

    @classmethod
    def on_create(
        cls,
        ticket,
        actor,
    ):
        NotificationService.trigger(
            "ticket.created",
            ticket=ticket,
            actor=actor,
        )

    @classmethod
    def on_update(
        cls,
        ticket,
        actor,
        changes,
    ):
        NotificationService.trigger(
            "ticket.updated",
            ticket=ticket,
            actor=actor,
            changes=changes,
        )