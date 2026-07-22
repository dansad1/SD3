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
        if status is None:
            return TicketStatusTransition.objects.none()

        queryset = (
            TicketStatusTransition.objects
            .filter(
                source=status,
            )
        )

        if role is not None:
            queryset = queryset.filter(
                allowed_roles=role,
            )

        return queryset.distinct()

    # =====================================================
    # AVAILABLE
    # =====================================================

    @classmethod
    def get_available_statuses(
        cls,
        status,
        role=None,
    ):
        if status is None:
            return set()

        allowed = set(
            cls.get_transitions(
                status=status,
                role=role,
            ).values_list(
                "target_id",
                flat=True,
            )
        )

        allowed.add(
            status.pk,
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
        if new_status is None:
            raise ValidationError({
                "status": [
                    "Статус заявки обязателен.",
                ],
            })

        if old_status is None:
            return

        if old_status.pk == new_status.pk:
            return

        allowed = set(
            cls.get_transitions(
                status=old_status,
                role=role,
            ).values_list(
                "target_id",
                flat=True,
            )
        )

        if new_status.pk not in allowed:
            raise ValidationError({
                "status": [
                    (
                        f"Переход "
                        f"{old_status} → {new_status} "
                        f"запрещён."
                    ),
                ],
            })

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
            and getattr(
                status,
                "comment_required",
                False,
            )
        )

    @classmethod
    def blocks_editing(
        cls,
        ticket,
    ):
        if ticket is None:
            return False

        status = ticket.get_value(
            "status",
        )

        return bool(
            status
            and getattr(
                status,
                "blocks_editing",
                False,
            )
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
            old_status is not None
            and old_status.pk == new_status.pk
        ):
            return

        if (
            cls.requires_comment(
                new_status,
            )
            and not str(
                comment or "",
            ).strip()
        ):
            raise ValidationError({
                "comment": [
                    (
                        "Для перехода в этот статус "
                        "требуется комментарий."
                    ),
                ],
            })