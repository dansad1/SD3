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

    # =====================================================
    # FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
        ctx,
    ):

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

    # =====================================================
    # RUN
    # =====================================================

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        print(
            "🔐 LOGIN PAYLOAD",
            payload
        )

        login_value = payload.get(
            "login"
        )

        password = payload.get(
            "password"
        )

        credentials = {

            User.USERNAME_FIELD:
                login_value,

            "password":
                password,

        }

        print(
            "🔐 LOGIN CREDENTIALS",
            credentials
        )

        user = authenticate(

            request,

            **credentials,

        )

        print(
            "👤 AUTH USER",
            user
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

        login(
            request,
            user,
        )

        print(
            "✅ LOGIN SUCCESS",
            request.user,
        )

        print(
            "🪪 SESSION",
            request.session.session_key
        )

        return {

            "status": "ok",

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