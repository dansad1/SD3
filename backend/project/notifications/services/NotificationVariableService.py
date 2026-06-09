# backend/project/notifications/services/NotificationVariableService.py

from backend.project.users.models import (
    UserField,
)

from backend.project.tickets.models import (
    TicketField,
)

from backend.project.companies.models import (
    CompanyField,
)


class NotificationVariableService:

    SYSTEM_VARIABLES = [

        "site_url",

        "support_email",

        "current_time",

        "temporary_password",

        "reset_link",
    ]

    @classmethod
    def get_available_variables(
        cls,
    ):
        return {

            "Пользователь":
                cls.get_user_variables(),

            "Компания":
                cls.get_company_variables(),

            "Заявка":
                cls.get_ticket_variables(),

            "Система":
                cls.SYSTEM_VARIABLES,
        }

    @classmethod
    def get_user_variables(
        cls,
    ):
        return [

            f"user_{name}"

            for name in cls._field_names(
                UserField
            )
        ]

    @classmethod
    def get_company_variables(
        cls,
    ):
        return [

            f"company_{name}"

            for name in cls._field_names(
                CompanyField
            )
        ]

    @classmethod
    def get_ticket_variables(
        cls,
    ):
        return [

            f"ticket_{name}"

            for name in cls._field_names(
                TicketField
            )
        ]

    @classmethod
    def _field_names(
        cls,
        model,
    ):
        return sorted({

            name

            for name in (

                model.objects

                .exclude(
                    name__isnull=True,
                )

                .exclude(
                    name="",
                )

                .values_list(
                    "name",
                    flat=True,
                )
            )

            if name
        })