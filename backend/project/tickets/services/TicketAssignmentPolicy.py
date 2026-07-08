from django.core.exceptions import (
    ValidationError,
)

from backend.project.users.models import (
    User,
)


class TicketAssignmentPolicy:

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

        qs = cls.get_executor_queryset()

        if actor.has_perm(
            "tickets.assign_any",
        ):
            return qs

        if actor.has_perm(
            "tickets.assign_self",
        ):
            return qs.filter(
                pk=actor.pk,
            )

        return User.objects.none()

    @classmethod
    def can_assign_executor(
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

    @classmethod
    def validate_executor(
        cls,
        actor,
        executor,
    ):

        if cls.can_assign_executor(
            actor,
            executor,
        ):
            return

        raise ValidationError(
            "Недопустимый исполнитель."
        )