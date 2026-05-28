# backend/auth/actions/LoginAction.py

from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
)

from rest_framework.exceptions import (
    ValidationError
)

from backend.engine.action.Base.BaseAction import (
    BaseAction
)

User = get_user_model()


class LoginAction(BaseAction):

    code = "login"

    permission = None

    def get_fields(self, request, ctx):

        return [
            {
                "name": "login",
                "label": "Логин",
                "type": "string",
                "required": True,
            },
            {
                "name": "password",
                "label": "Пароль",
                "type": "password",
                "required": True,
            },
        ]

    def run(self, request, payload, ctx):

        login_value = payload.get("login")
        password = payload.get("password")

        credentials = {
            User.USERNAME_FIELD: login_value,
            "password": password,
        }

        user = authenticate(
            request,
            **credentials,
        )

        if not user or not user.is_active:
            raise ValidationError({
                "password": [
                    "Неверный логин или пароль"
                ]
            })

        login(request, user)

        request.session.cycle_key()

        return {
            "status": "ok",

            "user": {
                "id": user.pk,
                "login": getattr(
                    user,
                    User.USERNAME_FIELD,
                ),
            },

            "effects": [
                {
                    "type": "auth.reload_user",
                },
                {
                    "type": "navigate",
                    "page": "/",
                },
            ],
        }