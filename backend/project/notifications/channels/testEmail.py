from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.utils.html import strip_tags

from backend.engine.action.Base.BaseAction import BaseAction
from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)


class SendTemplateEmailAction(BaseAction):
    code = "email.send_template"
    permission = "notifications.email.send"
    success_message = "Письма отправлены"

    def validate(
        self,
        request,
        payload,
        ctx,
    ):
        payload = dict(payload or {})

        if not payload.get("template"):
            raise ValidationError({
                "template": "Шаблон не указан",
            })

        if not payload.get("users"):
            raise ValidationError({
                "users": "Получатели не указаны",
            })

        context = payload.get("context", {})

        if not isinstance(context, dict):
            raise ValidationError({
                "context": "Ожидался объект",
            })

        payload["context"] = context

        return payload

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        email_template = payload["template"]
        context = payload["context"]
        users = payload["users"]

        recipients = [
            user.email
            for user in users
            if getattr(user, "email", None)
        ]

        recipients = EmailChannel.normalize_recipients(
            recipients
        )

        template_context = Context(
            context,
            autoescape=True,
        )

        subject = Template(
            email_template.subject
        ).render(
            template_context
        ).strip()

        body_html = Template(
            email_template.body
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
            recipients=recipients,
        )

        return {
            "status": "ok",
            "sent": sent_count,
        }