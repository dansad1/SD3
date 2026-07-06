from backend.engine.fields.utils.sync import (
    sync_m2m,
)

from backend.project.users.models import (
    User,
)


def get_service_users(
    service,
):
    users = User.objects.none()

    for company in service.companies.all():
        users |= User.objects.filter(
            dynamic_values__field__name="company",
            dynamic_values__value__contains=f'"value": {company.pk}',
        )

    return users.distinct()


def sync_service(
    service,
):
    sync_m2m(
        service.users,
        get_service_users(
            service,
        ),
    )