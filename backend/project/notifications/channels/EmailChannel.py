from collections.abc import Iterable

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.core.validators import validate_email

from backend.project.notifications.models import EmailSettings


class EmailChannel:
    @classmethod
    def get_settings(cls) -> EmailSettings:
        smtp_settings = (
            EmailSettings.objects
            .filter(is_active=True)
            .order_by("id")
            .first()
        )

        if smtp_settings is None:
            raise ImproperlyConfigured(
                "Активные SMTP-настройки не найдены"
            )

        return smtp_settings

    @classmethod
    def get_connection(
        cls,
        smtp_settings: EmailSettings | None = None,
    ) -> EmailBackend:
        smtp_settings = smtp_settings or cls.get_settings()

        return EmailBackend(
            host=smtp_settings.host,
            port=smtp_settings.port,
            username=smtp_settings.username or None,
            password=smtp_settings.password or None,
            use_tls=smtp_settings.use_tls,
            use_ssl=smtp_settings.use_ssl,
            timeout=smtp_settings.timeout,
            fail_silently=False,
        )

    @classmethod
    def normalize_recipients(
        cls,
        recipients: Iterable[str],
    ) -> list[str]:
        if isinstance(recipients, str):
            recipients = [recipients]

        result = []

        for recipient in recipients:
            recipient = str(recipient).strip().lower()

            if not recipient:
                continue

            validate_email(recipient)

            if recipient not in result:
                result.append(recipient)

        if not result:
            raise ValueError(
                "Не указан ни один получатель"
            )

        if len(result) > 100:
            raise ValueError(
                "Нельзя отправить письмо более чем "
                "100 получателям одновременно"
            )

        return result

    @classmethod
    def send_message(
        cls,
        subject: str,
        body: str,
        recipients: Iterable[str],
        html: str | None = None,
    ) -> int:
        smtp_settings = cls.get_settings()
        recipients = cls.normalize_recipients(
            recipients
        )

        subject = str(subject).strip()
        body = str(body or "")

        if not subject:
            raise ValueError(
                "Тема письма не указана"
            )

        if "\r" in subject or "\n" in subject:
            raise ValueError(
                "Тема письма содержит недопустимые символы"
            )

        connection = cls.get_connection(
            smtp_settings
        )

        message = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=smtp_settings.default_from,
            to=recipients,
            connection=connection,
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
    def test_connection(cls) -> None:
        connection = cls.get_connection()

        try:
            connection.open()
        finally:
            connection.close()