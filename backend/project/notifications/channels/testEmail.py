from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.utils.html import strip_tags

from backend.engine.action.Base.BaseAction import BaseAction
from backend.project.notifications.channels.EmailChannel import (
    EmailChannel,
)
from backend.project.notifications.models import (
    NotificationTemplate,
)
from backend.project.users.models import User


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
        payload = dict(
            payload
            or {}
        )

        template_id = payload.get(
            "template"
        )

        if isinstance(
            template_id,
            dict,
        ):
            template_id = (
                template_id.get("value")
                or template_id.get("id")
            )

        if not template_id:
            raise ValidationError({
                "template": "Шаблон не указан",
            })

        user_ids = payload.get(
            "users"
        )

        if not user_ids:
            raise ValidationError({
                "users": "Получатели не указаны",
            })

        if not isinstance(
            user_ids,
            list,
        ):
            raise ValidationError({
                "users": "Ожидался список",
            })

        context = payload.get(
            "context",
            {},
        )

        if not isinstance(
            context,
            dict,
        ):
            raise ValidationError({
                "context": "Ожидался объект",
            })

        payload["template"] = template_id
        payload["users"] = user_ids
        payload["context"] = context

        return payload

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        template_id = payload[
            "template"
        ]

        user_ids = self.extract_ids(
            payload["users"]
        )

        try:
            email_template = (
                NotificationTemplate.objects
                .get(
                    pk=template_id,
                )
            )

        except NotificationTemplate.DoesNotExist:
            raise ValidationError({
                "template":
                    "Шаблон не найден",
            })

        users = (
            User.objects
            .filter(
                pk__in=user_ids,
                is_active=True,
            )
            .exclude(
                email="",
            )
        )

        recipients = [
            user.email
            for user in users
            if user.email
        ]

        recipients = (
            EmailChannel
            .normalize_recipients(
                recipients
            )
        )

        template_context = Context(
            payload["context"],
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

        sent_count = (
            EmailChannel.send_message(
                subject=subject,
                body=body_text,
                html=body_html,
                recipients=recipients,
            )
        )

        return {
            "status": "ok",
            "sent": sent_count,
            "recipients": len(recipients),
        }

    def extract_ids(
        self,
        values,
    ):
        result = []

        for value in values:
            if isinstance(
                value,
                dict,
            ):
                value = (
                    value.get("value")
                    or value.get("id")
                )

            try:
                value = int(value)

            except (
                TypeError,
                ValueError,
            ):
                raise ValidationError({
                    "users":
                        "Некорректный получатель",
                })

            if value not in result:
                result.append(
                    value
                )

        if not result:
            raise ValidationError({
                "users":
                    "Получатели не указаны",
            })

        return result