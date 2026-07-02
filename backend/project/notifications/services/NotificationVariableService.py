# backend/project/notifications/services/variables.py

from backend.project.companies.models import (
    CompanyField,
)

from backend.project.tickets.models import (
    TicketField,
)

from backend.project.users.models import (
    UserField,
)


SYSTEM_VARIABLES = [

    "site_url",

    "support_email",

    "current_time",

    "temporary_password",

    "reset_link",

]


def get_available_variables():

    return {

        "Пользователь":
            get_user_variables(),

        "Компания":
            get_company_variables(),

        "Заявка":
            get_ticket_variables(),

        "Система":
            SYSTEM_VARIABLES,

    }


def get_user_variables():

    return [

        f"user_{name}"

        for name in _field_names(
            UserField,
        )

    ]


def get_company_variables():

    return [

        f"company_{name}"

        for name in _field_names(
            CompanyField,
        )

    ]


def get_ticket_variables():

    return [

        f"ticket_{name}"

        for name in _field_names(
            TicketField,
        )

    ]


def _field_names(
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