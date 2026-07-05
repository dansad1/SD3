from backend.project.companies.models import (
    Company,
)


def sync_user(
    user,
):
    company_id = user.get_value(
        "company",
    )

    if not company_id:
        return

    company = Company.objects.filter(
        pk=company_id,
    ).first()

    if not company:
        return

    for service in (
        company.services.all()
    ):
        service.users.add(
            user,
        )