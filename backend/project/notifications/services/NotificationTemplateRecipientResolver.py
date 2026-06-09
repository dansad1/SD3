# backend/project/notifications/services/NotificationTemplateRecipientResolver.py

class NotificationTemplateRecipientResolver:

    @classmethod
    def resolve(
        cls,
        template,
        context,
    ):
        if not template:
            return []

        if not hasattr(
            template,
            "special_users",
        ):
            return []

        return list(
            template.special_users.all()
        )