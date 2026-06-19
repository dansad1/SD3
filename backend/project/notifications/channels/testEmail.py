from backend.engine.action.Base.BaseAction import BaseAction
from backend.engine.fields.types.email import EmailFieldType
from backend.project.notifications.channels.SendEmailAction import SendEmailAction


class SendTestEmailAction(BaseAction):

    code = "email.send_test"

    permission = (
        "notifications.smtp.test"
    )

    success_message = (
        "Тестовое письмо отправлено"
    )

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

        SendEmailAction().submit(

            request=request,

            payload={

                "subject":
                    "SMTP test",

                "body":
                    "SMTP configured successfully.",

                "html": """
                    <h2>
                        SMTP configured successfully.
                    </h2>

                    <p>
                        This is a test message.
                    </p>
                """,

                "recipients": [

                    payload["email"],

                ],

            },

            ctx=ctx,

        )