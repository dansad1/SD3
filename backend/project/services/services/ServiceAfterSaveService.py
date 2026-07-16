from backend.project.services.entities.sync import (
    sync_service,
)


class ServiceAfterSaveService:

    @staticmethod
    def process(
        ctx,
    ):
        sync_service(
            ctx.instance,
        )

        return ctx