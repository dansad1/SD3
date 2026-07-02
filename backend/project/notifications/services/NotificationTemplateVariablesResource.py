from backend.engine.Resource.BaseResource import (
    BaseResource,
)
from backend.project.notifications.services.NotificationVariableService import get_available_variables


class NotificationTemplateVariablesResource(
    BaseResource,
):

    code = "notification_template.variables"

    def get(
        self,
        request,
        **kwargs,
    ):

        return {

            "title":
                "Доступные переменные",

            "groups": [

                {

                    "key":
                        group.lower(),

                    "label":
                        group,

                    "items": [

                        {

                            "key":
                                variable,

                            "label":
                                f"{{{{ {variable} }}}}",

                            "value":
                                variable,

                        }

                        for variable in variables

                    ],

                }

                for group, variables in (
                    get_available_variables().items()
                )

            ],

            "onInsert": {

                "type":
                    "form:setValue",

                "payload": {

                    "field":
                        "body",

                    "mode":
                        "append",

                    "value": {

                        "bind":
                            "value",

                        },

                },

            },

        }