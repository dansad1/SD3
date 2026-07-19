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

        channels = cls.get_channels(
            template
        )

        results = []

        for channel_code in channels:
            if channel_code == "email":
                result = cls.dispatch_email(
                    template=template,
                    context=context,
                    recipients=recipients,
                )

                results.append({
                    "channel": "email",
                    "result": result,
                })

        return {
            "status": "ok",
            "results": results,
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

        if channels:
            if isinstance(
                channels,
                str,
            ):
                return [
                    channels,
                ]

            return list(
                channels
            )

        channel = getattr(
            template,
            "channel",
            None,
        )

        if channel:
            return [
                channel,
            ]

        return []

    @classmethod
    def dispatch_email(
        cls,
        template,
        context,
        recipients,
    ):
        email_addresses = [
            user.email
            for user in recipients
            if getattr(
                user,
                "email",
                None,
            )
        ]

        email_addresses = (
            EmailChannel.normalize_recipients(
                email_addresses
            )
        )

        template_context = Context(
            context,
            autoescape=True,
        )

        subject = Template(
            template.subject
        ).render(
            template_context
        ).strip()

        body_html = Template(
            template.body
        ).render(
            template_context
        )

        body_text = strip_tags(
            body_html
        ).strip()

        sent_count = EmailChannel.send_message(
            subject=subject,
            body=body_text,
            html=body_html,
            recipients=email_addresses,
        )

        return {
            "sent": sent_count,
            "recipients": len(
                email_addresses
            ),
        }