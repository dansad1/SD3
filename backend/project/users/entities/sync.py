from backend.project.users.models import (
    User,
)


def sync_user(
    user,
    old_company=None,
):
    new_company = user.company

    #
    # REMOVE
    #

    if (
        old_company
        and old_company != new_company
    ):
        for service in (
            old_company.services.all()
        ):
            service.users.remove(
                user,
            )

    #
    # ADD
    #

    if new_company:

        for service in (
            new_company.services.all()
        ):
            service.users.add(
                user,
            )