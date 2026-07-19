from collections.abc import Iterable

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.core.validators import validate_email

from backend.project.notifications.models import EmailSettings


class EmailChannel:

    DEFAULT_TIMEOUT = 30
    MAX_RECIPIENTS = 100

    @classmethod
    def get_settings(
        cls,
    ) -> EmailSettings:
        settings = (
            EmailSettings.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "id",
            )
            .first()
        )

        if settings is None:
            raise ImproperlyConfigured(
                "Активные SMTP настройки не найдены"
            )

        return settings

    @classmethod
    def get_connection(
        cls,
        settings=None,
    ) -> EmailBackend:
        settings = (
            settings
            or cls.get_settings()
        )

        use_tls = (
            settings.encryption
            == EmailSettings.Encryption.TLS
        )

        use_ssl = (
            settings.encryption
            == EmailSettings.Encryption.SSL
        )

        return EmailBackend(
            host=settings.host,
            port=settings.port,
            username=(
                settings.host_user
                or None
            ),
            password=(
                settings.host_password
                or None
            ),
            use_tls=use_tls,
            use_ssl=use_ssl,
            timeout=cls.DEFAULT_TIMEOUT,
            fail_silently=False,
        )

    @classmethod
    def normalize_recipients(
        cls,
        recipients: Iterable[str],
    ) -> list[str]:
        if isinstance(
            recipients,
            str,
        ):
            recipients = [
                recipients,
            ]

        result = []

        for recipient in recipients:
            recipient = (
                str(recipient)
                .strip()
                .lower()
            )

            if not recipient:
                continue

            validate_email(
                recipient
            )

            if recipient not in result:
                result.append(
                    recipient
                )

        if not result:
            raise ValueError(
                "Не указан ни один получатель"
            )

        if len(result) > cls.MAX_RECIPIENTS:
            raise ValueError(
                "Слишком много получателей"
            )

        return result

    @classmethod
    def validate_subject(
        cls,
        subject,
    ) -> str:
        subject = str(
            subject
            or ""
        ).strip()

        if not subject:
            raise ValueError(
                "Тема письма не указана"
            )

        if (
            "\r" in subject
            or "\n" in subject
        ):
            raise ValueError(
                "Некорректная тема письма"
            )

        return subject

    @classmethod
    def send_message(
        cls,
        subject,
        body,
        recipients,
        html=None,
    ) -> int:
        settings = cls.get_settings()

        recipients = cls.normalize_recipients(
            recipients
        )

        subject = cls.validate_subject(
            subject
        )

        message = EmailMultiAlternatives(
            subject=subject,
            body=str(
                body
                or ""
            ),
            from_email=settings.default_from,
            to=recipients,
            connection=cls.get_connection(
                settings
            ),
        )

        if html:
            message.attach_alternative(
                str(html),
                "text/html",
            )

        return message.send(
            fail_silently=False
        )

    @classmethod
    def test_connection(
        cls,
    ) -> None:
        connection = cls.get_connection()

        try:
            connection.open()

        finally:
            connection.close()