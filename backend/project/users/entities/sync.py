from backend.project.companies.models import Company


def sync_user(user):
    company = user.get_value(
        "company",
    )

    user.services.clear()

    if not company:
        return

    if not isinstance(
        company,
        Company,
    ):
        raise TypeError(
            f"Expected Company, got {type(company).__name__}",
        )

    for service in company.services.all():
        service.users.add(
            user,
        )