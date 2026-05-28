from django.contrib.auth import (
    get_user_model
)

from django.contrib.auth.tokens import (
    default_token_generator
)

from django.utils.http import (
    urlsafe_base64_decode
)

from rest_framework.exceptions import (
    ValidationError
)

from backend.engine.action.Base.BaseAction import (
    BaseAction
)

User = get_user_model()


class PasswordResetConfirmAction(BaseAction):

    code = "password.reset.confirm"

    def get_fields(self, request, ctx):

        return [

            {
                "name": "uid",
                "type": "hidden",
                "required": True,
            },

            {
                "name": "token",
                "type": "hidden",
                "required": True,
            },

            {
                "name": "password",
                "label": "Новый пароль",
                "type": "password",
                "required": True,
            },

            {
                "name": "password2",
                "label": "Повторите пароль",
                "type": "password",
                "required": True,
            },

        ]

    def run(self, request, payload, ctx):

        password = payload["password"]
        password2 = payload["password2"]

        if password != password2:

            raise ValidationError({
                "password2": [
                    "Пароли не совпадают"
                ]
            })

        try:

            uid = (
                urlsafe_base64_decode(
                    payload["uid"]
                ).decode()
            )

            user = User.objects.get(pk=uid)

        except Exception:

            raise ValidationError({
                "__all__": [
                    "Неверная ссылка"
                ]
            })

        token = payload["token"]

        if not default_token_generator.check_token(
            user,
            token,
        ):

            raise ValidationError({
                "__all__": [
                    "Ссылка недействительна"
                ]
            })

        user.set_password(password)

        user.save()

        return {
            "status": "ok",

            "effects": [

                {
                    "type": "navigate",
                    "page": "/login",
                }

            ],
        }