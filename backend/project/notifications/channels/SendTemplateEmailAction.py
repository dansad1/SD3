import re
from django.template import Context, Template
from backend.engine.action.Base.BaseAction import BaseAction
from backend.project.notifications.channels.EmailChannel import EmailChannel


class SendTemplateEmailAction(BaseAction):
    code = "email.send_template"
    permission = "notifications.email.send"

    def run(self, request, payload, ctx, ):
        template = payload[
            "template"
        ]

        context = payload.get("context", {})
        users = payload["users"]
        recipients = [
            user.email
            for user in users
            if user.email
        ]
        subject = (Template(template.subject).render(Context(context)))
        body_html = (Template(template.body).render(
            Context(context)))
        body_text = re.sub(r"<[^>]+>", "", body_html, )
        EmailChannel.send_message(
            subject=subject,
            body=body_text,
            html=body_html,
            recipients=recipients,

        )

        return {"status": "ok",}
