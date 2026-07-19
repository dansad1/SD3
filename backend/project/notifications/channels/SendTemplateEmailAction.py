from backend.engine.action.Base.BaseAction import BaseAction
from backend.engine.fields.types.email import EmailFieldType
from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class SendTestEmailAction(BaseAction):
    code = "email.send_test"
    permission = "notifications.smtp.test"
    success_message = "Тестовое письмо отправлено"

    def get_fields(
        self,
        request,
        ctx,
    ):
        return [
            EmailFieldType(
                name="email",
                label="Email",
                required=True,
            ),
        ]

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        recipient = payload["email"]

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
            recipients=[recipient],
        )

        return {
            "status": "ok",
            "sent": sent_count,
        }