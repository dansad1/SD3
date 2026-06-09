# backend/project/notifications/services/NotificationContextBuilder.py

from django.conf import settings


class NotificationContextBuilder:

    @classmethod
    def build(
        cls,
        **kwargs,
    ):
        ctx = {}

        ctx.update(kwargs)

        ctx.setdefault(
            "site_url",
            getattr(
                settings,
                "SITE_URL",
                "",
            )
        )

        return ctx