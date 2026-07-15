from backend.project.companies.entities.sync import (
    sync_company,
)


class CompanyAfterSaveService:

    @classmethod
    def process(
        cls,
        ctx,
    ):
        sync_company(
            ctx.instance,
        )