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

        recipient = settings.default_from

        if not recipient:
            raise ValidationError({
                "__all__": (
                    "В SMTP настройках не указан "
                    "адрес отправителя"
                ),
            })

        sent_count = EmailChannel.send_message(
            subject="Проверка SMTP",
            body=(
                "SMTP настроен успешно.\n\n"
                "Это тестовое сообщение servicedesk."
            ),
            html=(
                "<h2>SMTP настроен успешно</h2>"
                "<p>"
                "Это тестовое сообщение servicedesk."
                "</p>"
            ),
            recipients=[
                recipient,
            ],
        )

        return {
            "status": "ok",
            "sent": sent_count,
            "recipient": recipient,
        }