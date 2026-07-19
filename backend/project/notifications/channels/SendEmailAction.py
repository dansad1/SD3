from django.core.exceptions import ValidationError

from backend.engine.action.Base.BaseAction import BaseAction
from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class SendTestEmailAction(BaseAction):

    code = "email.send_test"

    permission = "notifications.smtp.test"

    success_message = "Тестовое письмо отправлено"

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        settings = EmailChannel.get_settings()

        if not settings.default_from:
            raise ValidationError({
                "__all__": (
                    "Не указан адрес получателя"
                ),
            })

        sent_count = EmailChannel.send_message(
            subject="Проверка SMTP",
            body="SMTP настроен успешно.",
            html=(
                "<h2>SMTP настроен успешно</h2>"
                "<p>Тестовое письмо доставлено.</p>"
            ),
            recipients=[
                settings.default_from,
            ],
        )

        return {
            "status": "ok",
            "sent": sent_count,
        }