from django.core.mail import get_connection

from backend.engine.action.Base.BaseAction import BaseAction

from backend.project.notifications.models import (
    EmailSettings,
)


class TestEmailAction(

    BaseAction

):

    code = "email.test"

    permission = (
        "notifications.settings.edit"
    )

    success_message = (
        "SMTP подключение успешно"
    )

    def run(self,request,payload,ctx,):

        settings = (
            EmailSettings.objects
            .filter(
                is_active=True
            )
            .first()
        )

        if not settings:
            raise ValueError(
                "SMTP настройки отсутствуют"
            )

        connection = get_connection(
            host=settings.host,
            port=settings.port,
            username=settings.username,
            password=settings.password,
            use_tls=settings.use_tls,
            use_ssl=settings.use_ssl,
            timeout=settings.timeout,

        )

        connection.open()
        connection.close()

        return {

            "status": "ok",

        }
