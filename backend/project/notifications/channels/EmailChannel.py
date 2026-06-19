from django.core.mail import (
    EmailMultiAlternatives,
)
from django.core.mail.backends.smtp import (
    EmailBackend,
)

from backend.project.notifications.models import (
    EmailSettings,
)


class EmailChannel:

    @classmethod
    def get_settings(cls):

        settings = (
            EmailSettings.objects
            .filter(
                is_active=True,
            )
            .first()
        )

        if not settings:
            raise ValueError(
                "SMTP settings not configured"
            )

        return settings

    @classmethod
    def get_connection(cls):

        settings = cls.get_settings()
        return EmailBackend(
            host=settings.host,
            port=settings.port,
            username=settings.username,
            password=settings.password,
            use_tls=settings.use_tls,
            use_ssl=settings.use_ssl,
            timeout=settings.timeout,

        )

    @classmethod
    def send_message(
        cls,
        subject,
        body,
        recipients,
        html=None,
        from_email=None,

    ):

        settings = cls.get_settings()
        msg = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=(
                from_email
                or settings.default_from
            ),

            to=recipients,
            connection=cls.get_connection(),

        )
        if html:
            msg.attach_alternative(
                html,
                "text/html",

            )

        msg.send()

    @classmethod
    def test(cls):
        connection = cls.get_connection()
        connection.open()
        connection.close()