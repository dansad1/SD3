# backend/project/tickets/services/TicketTransitionService.py

from django.core.exceptions import (
    ValidationError,
)

from backend.project.tickets.models import (
    TicketStatusTransition,
)


class TicketTransitionService:

    # =====================================================
    # AVAILABLE STATUSES
    # =====================================================

    @classmethod
    def get_available_statuses(
        cls,
        ticket,
        role=None,
    ):
        if not ticket:
            return []

        if not ticket.status_id:
            return []

        transitions = (

            TicketStatusTransition.objects

            .filter(
                source=ticket.status,
            )
        )

        if role:

            transitions = (

                transitions.filter(
                    allowed_roles=role,
                )
            )

        allowed_ids = set(

            transitions.values_list(
                "target_id",
                flat=True,
            )
        )

        allowed_ids.add(
            ticket.status_id
        )

        return allowed_ids

    # =====================================================
    # VALIDATE
    # =====================================================

    @classmethod
    def validate_transition(
        cls,
        ticket,
        old_status,
        new_status,
        role=None,
    ):
        if not old_status:
            return

        if not new_status:
            return

        if old_status.id == new_status.id:
            return

        transitions = (

            TicketStatusTransition.objects

            .filter(
                source=old_status,
            )
        )

        if role:

            transitions = (

                transitions.filter(
                    allowed_roles=role,
                )
            )

        allowed_ids = set(

            transitions.values_list(
                "target_id",
                flat=True,
            )
        )

        if new_status.id not in allowed_ids:

            raise ValidationError(

                f"Переход "
                f"{old_status} → "
                f"{new_status} "
                f"запрещён."
            )

    # =====================================================
    # COMMENT REQUIRED
    # =====================================================

    @classmethod
    def requires_comment(
        cls,
        status,
    ):
        if not status:
            return False

        return bool(
            status.comment_required
        )

    # =====================================================
    # BLOCK EDITING
    # =====================================================

    @classmethod
    def blocks_editing(
        cls,
        ticket,
    ):
        if not ticket:
            return False

        if not ticket.status_id:
            return False

        return bool(
            ticket.status.blocks_editing
        )

    # =====================================================
    # VALIDATE CHANGE
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
                new_status
            )
            and not comment
        ):
            raise ValidationError(
                "Требуется комментарий."
            )