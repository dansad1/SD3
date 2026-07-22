# backend/project/notifications/services/
# NotificationDispatcher.py

from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.utils.html import strip_tags

from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class NotificationDispatcher:

    CHANNELS = {
        "email": EmailChannel,
    }

    @classmethod
    def dispatch(
        cls,
        rule,
        context,
        recipients,
    ):
        template = rule.template

        if template is None:
            return {
                "status": "skipped",
                "reason": "template_not_configured",
            }

        if not getattr(
            template,
            "is_active",
            False,
        ):
            return {
                "status": "skipped",
                "reason": "template_inactive",
            }

        channel_code = str(
            rule.channel
            or ""
        ).strip()

        if not channel_code:
            return {
                "status": "skipped",
                "reason": "channel_not_configured",
            }

        if channel_code not in cls.CHANNELS:
            return {
                "status": "skipped",
                "reason": "channel_not_supported",
                "channel": channel_code,
            }

        template_channels = cls.get_channels(
            template,
        )

        if channel_code not in template_channels:
            return {
                "status": "skipped",
                "reason": "template_channel_not_supported",
                "channel": channel_code,
            }

        if not recipients:
            return {
                "status": "skipped",
                "reason": "recipients_not_found",
                "channel": channel_code,
            }

        if channel_code == "email":
            result = cls.dispatch_email(
                template=template,
                context=context,
                recipients=recipients,
            )

            return {
                "status": "ok",
                "channel": channel_code,
                "result": result,
            }

        return {
            "status": "skipped",
            "reason": "channel_not_implemented",
            "channel": channel_code,
        }

    @classmethod
    def get_channels(
        cls,
        template,
    ):
        channels = getattr(
            template,
            "channels",
            None,
        )

        if isinstance(
            channels,
            str,
        ):
            channels = [
                channels,
            ]

        if channels:
            return [
                str(channel).strip()
                for channel in channels
                if str(channel).strip()
            ]

        channel = getattr(
            template,
            "channel",
            None,
        )

        if channel:
            return [
                str(channel).strip(),
            ]

        return []

    @classmethod
    def dispatch_email(
            cls,
            template,
            context,
            recipients,
    ):
        template_context = Context(
            context,
            autoescape=True,
        )

        subject = Template(
            str(
                template.subject
                or ""
            )
        ).render(
            template_context,
        ).strip()

        body_html = Template(
            str(
                template.body
                or ""
            )
        ).render(
            template_context,
        )

        body_text = strip_tags(
            body_html,
        ).strip()

        if not subject:
            raise ValidationError(
                "После обработки шаблона тема письма пустая"
            )

        email_addresses = []

        for user in recipients:
            email = cls.get_user_email(
                user,
            )

            if email:
                email_addresses.append(
                    email,
                )

        email_addresses = list(
            dict.fromkeys(
                email_addresses,
            )
        )

        if not email_addresses:
            return {
                "sent": 0,
                "recipients": 0,
                "failed": 0,
            }

        sent_count = 0
        failed = []

        for email in email_addresses:
            try:
                sent_count += (
                    EmailChannel.send_message(
                        subject=subject,
                        body=body_text,
                        html=body_html,
                        recipients=[
                            email,
                        ],
                    )
                )

            except Exception as exc:
                failed.append({
                    "email": email,
                    "error": str(
                        exc
                    ),
                })

        return {
            "sent": sent_count,
            "recipients": len(
                email_addresses,
            ),
            "failed": len(
                failed,
            ),
            "failures": failed,
        }
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