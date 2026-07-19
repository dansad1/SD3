from django.core.exceptions import ValidationError

from backend.engine.action.Base.BaseAction import BaseAction
from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class SendEmailAction(BaseAction):
    code = "email.send"
    permission = "notifications.email.send"
    success_message = "Письмо отправлено"

    def validate(
        self,
        request,
        payload,
        ctx,
    ):
        payload = dict(payload or {})

        required_fields = (
            "subject",
            "body",
            "recipients",
        )

        for field_name in required_fields:
            if not payload.get(field_name):
                raise ValidationError({
                    field_name: "Обязательное поле",
                })

        recipients = payload["recipients"]

        if not isinstance(
            recipients,
            (list, tuple, set),
        ):
            raise ValidationError({
                "recipients":
                    "Ожидался список email-адресов",
            })

        payload["recipients"] = (
            EmailChannel.normalize_recipients(
                recipients
            )
        )

        return payload

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        sent_count = EmailChannel.send_message(
            subject=payload["subject"],
            body=payload["body"],
            html=payload.get("html"),
            recipients=payload["recipients"],
        )

        return {
            "status": "ok",
            "sent": sent_count,
        }