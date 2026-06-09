# backend/project/tickets/services/TicketAssignmentPolicy.py

from backend.project.users.models import (
    User,
    UserRole,
    UserField,
    UserFieldValue,
)


class TicketAssignmentPolicy:

    @classmethod
    def get_executor_queryset(cls):

        role_field = (
            UserField.objects
            .filter(
                name="role",
            )
            .first()
        )

        if not role_field:
            return User.objects.none()

        executor_roles = list(
            UserRole.objects.filter(
                is_executor=True,
            )
        )

        if not executor_roles:
            return User.objects.none()

        executor_ids = {
            str(role.id)
            for role in executor_roles
        }

        executor_names = {
            role.name
            for role in executor_roles
        }

        valid_values = (
            executor_ids
            |
            executor_names
        )

        user_ids = (
            UserFieldValue.objects
            .filter(
                field=role_field,
                value__in=valid_values,
            )
            .values_list(
                "user_id",
                flat=True,
            )
        )

        return User.objects.filter(
            id__in=set(user_ids)
        )

    @classmethod
    def get_allowed_assignees(
        cls,
        actor,
    ):
        qs = cls.get_executor_queryset()

        if actor.has_perm(
            "tickets.assign_any"
        ):
            return qs

        if actor.has_perm(
            "tickets.assign_self"
        ):
            return qs.filter(
                id=actor.id,
            )

        return User.objects.none()

    @classmethod
    def can_assign(
        cls,
        actor,
        assignee,
    ):
        if not assignee:
            return True

        return cls.get_allowed_assignees(
            actor
        ).filter(
            id=assignee.id
        ).exists()