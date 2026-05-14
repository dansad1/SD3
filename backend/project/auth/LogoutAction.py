# backend/auth/actions/LogoutAction.py

from django.contrib.auth import logout

from backend.engine.action.Base.BaseAction import (
    BaseAction
)


class LogoutAction(BaseAction):

    code = "logout"

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        logout(request)

        return {

            "status": "ok",

            "effects": [

                {
                    "type": "auth.reload_user",
                },

                {
                    "type": "navigate",

                    "page": "/login",
                },

            ],
        }