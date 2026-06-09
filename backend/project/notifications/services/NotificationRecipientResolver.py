# backend/project/notifications/services/NotificationRecipientResolver.py

from backend.project.notifications.services.NotificationDefaultRecipientResolver import (
    NotificationDefaultRecipientResolver,
)

from backend.project.notifications.services.NotificationLogicalRecipientResolver import (
    NotificationLogicalRecipientResolver,
)

from backend.project.notifications.services.NotificationTemplateRecipientResolver import (
    NotificationTemplateRecipientResolver,
)


class NotificationRecipientResolver:

    @classmethod
    def resolve(
        cls,
        rule,
        event_code,
        context,
    ):
        users = []

        # шаблон

        users.extend(

            NotificationTemplateRecipientResolver.resolve(
                rule.template,
                context,
            )
        )

        # событие

        users.extend(

            NotificationDefaultRecipientResolver.resolve(
                event_code,
                context,
            )
        )

        # logical_role

        if rule.logical_role:

            users.extend(

                NotificationLogicalRecipientResolver.resolve(
                    rule.logical_role,
                    context,
                )
            )

        # role filter

        if rule.role_id:

            users = [

                user

                for user in users

                if getattr(
                    user,
                    "role_id",
                    None,
                )
                ==
                rule.role_id
            ]

        result = {}

        for user in users:

            if not user:
                continue

            result[user.id] = user

        return list(
            result.values()
        )