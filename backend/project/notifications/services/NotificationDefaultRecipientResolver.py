# backend/project/notifications/services/NotificationDefaultRecipientResolver.py

class NotificationDefaultRecipientResolver:

    EVENT_RECIPIENTS = {

        "ticket.created": [
            "requester",
        ],

        "ticket.comment_added": [
            "requester",
            "assignee",
        ],

        "ticket.assignee_changed": [
            "assignee",
        ],

        "ticket.status_changed": [
            "requester",
            "assignee",
        ],
    }

    @classmethod
    def resolve(
        cls,
        event_code,
        context,
    ):
        recipients = []

        for logical_role in cls.EVENT_RECIPIENTS.get(
            event_code,
            [],
        ):
            recipients.extend(
                NotificationLogicalRecipientResolver.resolve(
                    logical_role,
                    context,
                )
            )

        return recipients