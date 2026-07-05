from backend.engine.fields.utils.sync import sync_m2m
from backend.project.users.models import (
    User,
)


def get_service_users(
    service,
):
    users = set(
        service.users.all()
    )

    for company in (
        service.companies.all()
    ):
        users.update(
            User.objects.filter(
                company=company,
            )
        )

    return users


def sync_service(
    service,
):
    sync_m2m(
        service.users,
        get_service_users(
            service,
        ),
    )