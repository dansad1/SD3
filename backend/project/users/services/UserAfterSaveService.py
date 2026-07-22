from django.db import transaction

from backend.project.users.entities.sync import (
    sync_user,
)
from backend.project.users.services.UserNotificationService import (
    UserNotificationService,
)


class UserAfterSaveService:

    @classmethod
    def process(
        cls,
        ctx,
    ):
        target_user = ctx.instance

        # Синхронизация динамических данных выполняется сразу.
        sync_user(
            target_user,
        )

        created = (
            getattr(
                ctx,
                "mode",
                None,
            )
            == "create"
        )

        changes = getattr(
            ctx,
            "changes",
            None,
        )

        if hasattr(
            changes,
            "to_list",
        ):
            changes = changes.to_list()

        changes = changes or []

        password_changed = bool(
            getattr(
                ctx,
                "password_changed",
                False,
            )
        )

        actor = getattr(
            ctx.request,
            "user",
            None,
        )

        def notify():

            UserNotificationService.process(
                target_user=target_user,
                created=created,
                changes=changes,
                actor=actor,
                password_changed=password_changed,
            )

        transaction.on_commit(
            notify,
        )

        return ctx