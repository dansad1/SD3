# backend/project/notifications/services/NotificationLogicalRecipientResolver.py

class NotificationLogicalRecipientResolver:

    @classmethod
    def resolve(
        cls,
        logical_role,
        context,
    ):
        ticket = context.get(
            "ticket"
        )

        if not ticket:
            return []

        if logical_role == "requester":

            if ticket.created_by_id:
                return [
                    ticket.created_by
                ]

        elif logical_role == "assignee":

            if ticket.assigned_to_id:
                return [
                    ticket.assigned_to
                ]

        return []