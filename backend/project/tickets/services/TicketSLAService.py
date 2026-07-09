from datetime import timedelta

from django.utils import timezone

from backend.project.tickets.models import (
    TicketSLA,
)


class TicketSLAService:

    def __init__(
        self,
        ticket,
    ):
        self.ticket = ticket

    # =====================================================
    # HELPERS
    # =====================================================

    def get_priority(
        self,
    ):
        return self.ticket.get_value(
            "priority",
        )

    def get_status(
        self,
    ):
        return self.ticket.get_value(
            "status",
        )

    # =====================================================
    # SLA
    # =====================================================

    def get_sla_rule(
        self,
    ):
        if not self.ticket.type_id:
            return None

        priority = self.get_priority()

        if not priority:
            return None

        return (
            TicketSLA.objects
            .filter(
                type=self.ticket.type,
                priority=priority,
            )
            .first()
        )

    def compute_deadline(
        self,
        base_datetime=None,
    ):
        rule = self.get_sla_rule()

        if not rule:
            return None

        base = (
            base_datetime
            or self.ticket.created_at
            or timezone.now()
        )

        return (
            base
            + timedelta(
                hours=rule.hours,
            )
        )

    def recalculate(
        self,
        force=False,
    ):
        deadline = self.compute_deadline(
            base_datetime=self.ticket.created_at,
        )

        if deadline is None:
            return None

        current = self.ticket.get_value(
            "due_date",
        )

        if (
            not force
            and current == deadline
        ):
            return deadline

        self.ticket.set_value(
            "due_date",
            deadline,
        )

        return deadline

    # =====================================================
    # STATE
    # =====================================================

    def is_paused(
        self,
    ):
        status = self.get_status()

        if not status:
            return False

        return bool(
            getattr(
                status,
                "blocks_time",
                False,
            )
        )

    def is_overdue(
        self,
    ):
        deadline = self.ticket.get_value(
            "due_date",
        )

        if not deadline:
            return False

        if self.is_paused():
            return False

        return (
            timezone.now()
            > deadline
        )

    def get_remaining_seconds(
        self,
    ):
        deadline = self.ticket.get_value(
            "due_date",
        )

        if not deadline:
            return None

        if self.is_paused():
            return None

        delta = (
            deadline
            - timezone.now()
        )

        return int(
            delta.total_seconds(),
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def get_summary(
        self,
    ):
        return {
            "due_date": self.ticket.get_value(
                "due_date",
            ),
            "is_overdue": self.is_overdue(),
            "is_paused": self.is_paused(),
            "remaining_seconds": (
                self.get_remaining_seconds()
            ),
        }