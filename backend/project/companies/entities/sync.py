from backend.project.services.entities.sync import sync_service
from backend.project.users.models import (
    User,
)



def sync_company(
    company,
):
    #
    # Все сервисы компании
    #

    for service in (
        company.services.all()
    ):
        sync_service(
            service,
        )