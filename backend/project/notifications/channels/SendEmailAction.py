from backend.engine.action.Base.BaseAction import BaseAction
from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class SendEmailAction(BaseAction):

    code = "email.send"

    permission = (
        "notifications.email.send"
    )

    success_message = (
        "Письмо отправлено"
    )

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        EmailChannel.send_message(

            subject=payload["subject"],

            body=payload["body"],

            html=payload.get(
                "html",
            ),

            recipients=payload[
                "recipients"
            ],

            from_email=payload.get(
                "from_email",
            ),

        )