# backend/project/notifications/services/
# NotificationLogicalRecipientResolver.py


class NotificationLogicalRecipientResolver:

    @classmethod
    def resolve(
        cls,
        logical_role,
        context,
    ):
        if logical_role == "target_user":
            user = context.get(
                "user",
            )

            return [
                user,
            ] if user else []

        if logical_role == "actor":
            user = context.get(
                "actor",
            )

            return [
                user,
            ] if user else []

        ticket = context.get(
            "ticket",
        )

        if not ticket:
            return []

        if logical_role == "requester":
            if getattr(
                ticket,
                "created_by_id",
                None,
            ):
                return [
                    ticket.created_by,
                ]

        elif logical_role == "assignee":
            if getattr(
                ticket,
                "assigned_to_id",
                None,
            ):
                return [
                    ticket.assigned_to,
                ]

        return []