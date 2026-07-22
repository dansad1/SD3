# backend/project/notifications/services/
# NotificationRecipientResolver.py

from backend.project.notifications.services.NotificationLogicalRecipientResolver import (
    NotificationLogicalRecipientResolver,
)
from backend.project.notifications.services.NotificationTemplateRecipientResolver import (
    NotificationTemplateRecipientResolver,
)
from backend.project.users.models import User


class NotificationRecipientResolver:

    @classmethod
    def resolve(
        cls,
        rule,
        event_code,
        context,
    ):
        users = []

        # =================================================
        # MATRIX RECIPIENT
        # =================================================

        if rule.role_id:
            users.extend(
                User.objects.filter(
                    role_id=rule.role_id,
                    is_active=True,
                )
            )

        elif rule.logical_role:
            users.extend(
                NotificationLogicalRecipientResolver.resolve(
                    logical_role=rule.logical_role,
                    context=context,
                )
                or []
            )

        # =================================================
        # TEMPLATE SPECIAL USERS
        # =================================================

        if rule.template_id:
            users.extend(
                NotificationTemplateRecipientResolver.resolve(
                    rule.template,
                    context,
                )
                or []
            )

        # =================================================
        # NORMALIZE
        # =================================================

        return cls.normalize(
            users=users,
            channel=rule.channel,
        )

    @classmethod
    def normalize(
        cls,
        *,
        users,
        channel,
    ):
        result = {}

        for user in users:
            if not user:
                continue

            user_id = getattr(
                user,
                "pk",
                None,
            )

            if not user_id:
                continue

            if not getattr(
                user,
                "is_active",
                False,
            ):
                continue

            if channel == "email":
                email = cls.get_user_email(
                    user,
                )

                if not email:
                    continue

            result[user_id] = user

        return list(
            result.values()
        )

    @classmethod
    def get_user_email(
        cls,
        user,
    ):
        value = ""

        if hasattr(
            user,
            "get_value",
        ):
            value = user.get_value(
                "email",
            )

        if not value:
            value = getattr(
                user,
                "email",
                "",
            )

        return str(
            value
            or ""
        ).strip()