from django.contrib.auth.tokens import (
    default_token_generator
)

from django.contrib.auth import (
    get_user_model
)

from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from backend.engine.action.Base.BaseAction import (
    BaseAction
)

User = get_user_model()


class PasswordResetRequestAction(BaseAction):

    code = "password.reset.request"

    def get_fields(self, request, ctx):

        return [

            {
                "name": "email",

                "label": "Email",

                "type": "email",

                "required": True,
            }

        ]

    def run(self, request, payload, ctx):

        email = (
            payload.get("email") or ""
        ).strip().lower()

        user = (
            User.objects
            .filter(email=email)
            .first()
        )

        # 🔥 ВСЕГДА одинаковый ответ
        if user and user.is_active:

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = (
                default_token_generator
                .make_token(user)
            )

            reset_url = (
                f"https://app/reset-password-confirm"
                f"?uid={uid}"
                f"&token={token}"
            )

            send_mail(
                "Сброс пароля",
                f"Ссылка:\n{reset_url}",
                None,
                [user.email],
            )

        return {
            "status": "ok",

            "message":
                "Если пользователь существует — письмо отправлено",
        }