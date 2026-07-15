from backend.project.users.entities.sync import (
    sync_user,
)


class UserAfterSaveService:

    @classmethod
    def process(
        cls,
        ctx,
    ):

        sync_user(
            ctx.instance,
        )