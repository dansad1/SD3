from django.core.exceptions import (
    ValidationError,
)

from backend.project.tickets.models import (
    TicketStatusTransition,
)


class StatusTransitionService:

    # =====================================================
    # TRANSITIONS
    # =====================================================

    @classmethod
    def get_transitions(
        cls,
        status,
        role=None,
    ):
        if not status:
            return (
                TicketStatusTransition.objects.none()
            )

        queryset = (

            TicketStatusTransition.objects

            .filter(
                source=status,
            )

        )

        if role:

            queryset = queryset.filter(
                allowed_roles=role,
            )

        return queryset

    # =====================================================
    # AVAILABLE
    # =====================================================

    @classmethod
    def get_available_statuses(
        cls,
        ticket,
        role=None,
    ):
        if (
            not ticket
            or not ticket.status_id
        ):
            return set()

        allowed = set(

            cls.get_transitions(
                ticket.status,
                role,
            )

            .values_list(
                "target_id",
                flat=True,
            )

        )

        allowed.add(
            ticket.status_id,
        )

        return allowed

    # =====================================================
    # VALIDATION
    # =====================================================

    @classmethod
    def validate_transition(
        cls,
        ticket,
        old_status,
        new_status,
        role=None,
    ):
        if (
            not old_status
            or not new_status
            or old_status.pk == new_status.pk
        ):
            return

        allowed = set(

            cls.get_transitions(
                old_status,
                role,
            )

            .values_list(
                "target_id",
                flat=True,
            )

        )

        if new_status.pk not in allowed:

            raise ValidationError(

                f"Переход "
                f"{old_status} → "
                f"{new_status} "
                f"запрещён."

            )

    # =====================================================
    # RULES
    # =====================================================

    @classmethod
    def requires_comment(
        cls,
        status,
    ):
        return bool(
            status
            and status.comment_required
        )

    @classmethod
    def blocks_editing(
        cls,
        ticket,
    ):
        return bool(
            ticket
            and ticket.status_id
            and ticket.status.blocks_editing
        )

    # =====================================================
    # CHANGE
    # =====================================================

    @classmethod
    def validate_change(
        cls,
        ticket,
        old_status,
        new_status,
        role=None,
        comment=None,
    ):
        cls.validate_transition(
            ticket=ticket,
            old_status=old_status,
            new_status=new_status,
            role=role,
        )

        if (
            cls.requires_comment(
                new_status,
            )
            and not comment
        ):
            raise ValidationError(
                "Требуется комментарий.",
            )