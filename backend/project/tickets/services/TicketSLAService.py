# backend/project/tickets/services/TicketSLAService.py

from datetime import timedelta

from django.utils import timezone

from backend.project.tickets.models import (
    TicketSLA,
)


class TicketSLAService:
    """
    SLA теперь работает от реальных FK:
    ticket.status
    ticket.priority
    ticket.type

    Без поиска status/priority в dynamic fields.
    """

    def __init__(self, ticket):
        self.ticket = ticket

    def get_sla_rule(self):
        if not self.ticket.type_id:
            return None

        if not self.ticket.priority_id:
            return None

        return (
            TicketSLA.objects
            .filter(
                type=self.ticket.type,
                priority=self.ticket.priority,
            )
            .first()
        )

    def compute_deadline(self, base_datetime=None):
        rule = self.get_sla_rule()

        if not rule:
            return None

        base = base_datetime or self.ticket.created_at or timezone.now()

        return base + timedelta(hours=rule.hours)

    def recalculate(self, force=False):
        """
        Пересчитывает deadline только если есть SLA.
        """

        deadline = self.compute_deadline(
            base_datetime=self.ticket.created_at,
        )

        if not deadline:
            return None

        if not force and self.ticket.deadline == deadline:
            return deadline

        self.ticket.deadline = deadline

        self.ticket.save(
            update_fields=[
                "deadline",
            ]
        )

        return deadline

    def is_paused(self):
        status = self.ticket.status

        if not status:
            return False

        return bool(
            getattr(
                status,
                "blocks_time",
                False,
            )
        )

    def is_overdue(self):
        if not self.ticket.deadline:
            return False

        if self.is_paused():
            return False

        return timezone.now() > self.ticket.deadline

    def get_remaining_seconds(self):
        if not self.ticket.deadline:
            return None

        if self.is_paused():
            return None

        delta = self.ticket.deadline - timezone.now()

        return int(delta.total_seconds())

    def get_summary(self):
        return {
            "deadline": self.ticket.deadline,
            "is_overdue": self.is_overdue(),
            "is_paused": self.is_paused(),
            "remaining_seconds": self.get_remaining_seconds(),
        }