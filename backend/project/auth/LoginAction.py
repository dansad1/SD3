# backend/auth/actions/LoginAction.py

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from backend.engine.action.Base.BaseAction import BaseAction


class LoginAction(BaseAction):

    code = "login"

    def get_fields(self, request, ctx):
        return [
            {
                "name": "username",
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

        username = payload.get("username")
        password = payload.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if not user:
            raise ValidationError({
                "password": [
                    "Неверный логин или пароль"
                ]
            })

        if not user.is_active:
            raise ValidationError({
                "__all__": [
                    "Пользователь отключен"
                ]
            })

        login(request, user)

        return {
            "status": "ok",
            "user_id": user.pk,
        }