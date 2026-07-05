from backend.project.services.entities.sync import (
    sync_service,
)


def sync_company(
    company,
):
    for service in (
        company.services.all()
    ):
        sync_service(
            service,
        )