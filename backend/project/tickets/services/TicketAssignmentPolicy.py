from django.core.exceptions import (
    ValidationError,
)

from backend.project.users.models import (
    User,
)


class TicketAssignmentService:

    # =====================================================
    # QUERYSETS
    # =====================================================

    @classmethod
    def get_executor_queryset(
        cls,
    ):
        return (
            User.objects
            .filter(
                is_active=True,
                role__is_active=True,
                role__is_executor=True,
            )
            .select_related(
                "role",
            )
        )

    @classmethod
    def get_allowed_executors(
        cls,
        actor,
    ):
        if (
            not actor
            or not actor.is_authenticated
        ):
            return User.objects.none()

        queryset = (
            cls.get_executor_queryset()
        )

        if actor.has_perm(
            "tickets.assign_any",
        ):
            return queryset

        if actor.has_perm(
            "tickets.assign_self",
        ):
            return queryset.filter(
                pk=actor.pk,
            )

        return User.objects.none()

    # =====================================================
    # CHECKS
    # =====================================================

    @classmethod
    def can_assign(
        cls,
        actor,
        executor,
    ):
        if not executor:
            return True

        return (
            cls.get_allowed_executors(
                actor,
            )
            .filter(
                pk=executor.pk,
            )
            .exists()
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    @classmethod
    def validate_executor(
        cls,
        actor,
        executor,
    ):
        if (
            not cls.can_assign(
                actor,
                executor,
            )
        ):
            raise ValidationError(
                "Недопустимый исполнитель.",
            )

    @classmethod
    def validate_executors(
        cls,
        actor,
        executors,
    ):
        if not executors:
            return

        allowed = set(

            cls.get_allowed_executors(
                actor,
            )
            .values_list(
                "pk",
                flat=True,
            )

        )

        for executor in executors:

            if executor.pk not in allowed:

                raise ValidationError(
                    "Недопустимый исполнитель.",
                )