# backend/project/notifications/services/NotificationDispatcher.py

from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class NotificationDispatcher:

    CHANNELS = {

        "email":
            EmailChannel,
    }

    @classmethod
    def dispatch(
        cls,
        rule,
        context,
        recipients,
    ):
        template = rule.template

        if not template:
            return None

        channel = cls.CHANNELS.get(
            template.channel
        )

        if not channel:
            return None

        return channel.send(

            template=template,

            context=context,

            users=recipients,
        )