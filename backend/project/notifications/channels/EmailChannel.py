# backend/project/notifications/channels/EmailChannel.py

import re

from django.core.mail import (
    EmailMultiAlternatives,
)

from django.core.mail.backends.smtp import (
    EmailBackend,
)

from django.template import (
    Context,
    Template,
)

from backend.project.notifications.models import (
    EmailSettings,
)


class EmailChannel:

    @classmethod
    def send(
        cls,
        template,
        context,
        users,
    ):
        emails = [

            user.email

            for user in users

            if getattr(
                user,
                "email",
                None,
            )
        ]

        if not emails:
            return

        settings_obj = (
            EmailSettings.objects
            .first()
        )

        if not settings_obj:
            return

        subject = (
            Template(
                template.subject
            )
            .render(
                Context(
                    context
                )
            )
        )

        body_html = (
            Template(
                template.body
            )
            .render(
                Context(
                    context
                )
            )
        )

        body_text = re.sub(
            r"<[^>]+>",
            "",
            body_html,
        )

        connection = EmailBackend(

            host=settings_obj.host,

            port=settings_obj.port,

            username=settings_obj.host_user,

            password=settings_obj.host_password,

            use_tls=settings_obj.use_tls,

            use_ssl=settings_obj.use_ssl,
        )

        msg = EmailMultiAlternatives(

            subject=subject,

            body=body_text,

            from_email=settings_obj.default_from,

            to=emails,

            connection=connection,
        )

        msg.attach_alternative(
            body_html,
            "text/html",
        )

        msg.send()