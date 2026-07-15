from datetime import timedelta

from django.utils import timezone

from backend.project.tickets.models import (
    TicketSLA,
)


class TicketSLAService:

    # =====================================================
    # HELPERS
    # =====================================================

    @classmethod
    def get_priority(
        cls,
        ticket,
    ):
        return ticket.get_value(
            "priority",
        )

    @classmethod
    def get_status(
        cls,
        ticket,
    ):
        return ticket.get_value(
            "status",
        )

    # =====================================================
    # RULE
    # =====================================================

    @classmethod
    def get_sla_rule(
        cls,
        ticket,
    ):
        if not ticket.type_id:
            return None

        priority = cls.get_priority(
            ticket,
        )

        if not priority:
            return None

        return (
            TicketSLA.objects
            .filter(
                type=ticket.type,
                priority=priority,
            )
            .first()
        )

    # =====================================================
    # DEADLINE
    # =====================================================

    @classmethod
    def compute_deadline(
        cls,
        ticket,
        base_datetime=None,
    ):
        rule = cls.get_sla_rule(
            ticket,
        )

        if not rule:
            return None

        base = (
            base_datetime
            or ticket.created_at
            or timezone.now()
        )

        return (
            base
            + timedelta(
                hours=rule.hours,
            )
        )

    @classmethod
    def update_deadline(
        cls,
        ticket,
        force=False,
    ):
        deadline = cls.compute_deadline(
            ticket,
            base_datetime=ticket.created_at,
        )

        if deadline is None:
            return None

        current = ticket.get_value(
            "due_date",
        )

        if (
            not force
            and current == deadline
        ):
            return deadline

        ticket.set_value(
            "due_date",
            deadline,
        )

        return deadline

    # =====================================================
    # STATE
    # =====================================================

    @classmethod
    def is_paused(
        cls,
        ticket,
    ):
        status = cls.get_status(
            ticket,
        )

        if not status:
            return False

        return bool(
            getattr(
                status,
                "blocks_time",
                False,
            )
        )

    @classmethod
    def is_overdue(
        cls,
        ticket,
    ):
        deadline = ticket.get_value(
            "due_date",
        )

        if not deadline:
            return False

        if cls.is_paused(
            ticket,
        ):
            return False

        return (
            timezone.now()
            > deadline
        )

    @classmethod
    def get_remaining_seconds(
        cls,
        ticket,
    ):
        deadline = ticket.get_value(
            "due_date",
        )

        if not deadline:
            return None

        if cls.is_paused(
            ticket,
        ):
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

    @classmethod
    def get_summary(
        cls,
        ticket,
    ):
        return {
            "due_date": ticket.get_value(
                "due_date",
            ),
            "is_overdue": cls.is_overdue(
                ticket,
            ),
            "is_paused": cls.is_paused(
                ticket,
            ),
            "remaining_seconds": (
                cls.get_remaining_seconds(
                    ticket,
                )
            ),
        }