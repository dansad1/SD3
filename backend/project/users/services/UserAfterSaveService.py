import logging

from django.db import transaction

from backend.project.users.entities.sync import (
    sync_user,
)
from backend.project.users.models import User
from backend.project.users.services.UserNotificationService import (
    UserNotificationService,
)


logger = logging.getLogger(
    __name__,
)


class UserAfterSaveService:

    @classmethod
    def process(
        cls,
        ctx,
    ):
        target_user = ctx.instance

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

        target_user_id = target_user.pk
        actor_id = getattr(
            actor,
            "pk",
            None,
        )

        def notify():
            try:
                fresh_target_user = (
                    User.objects
                    .select_related(
                        "role",
                        "fieldset",
                    )
                    .prefetch_related(
                        "dynamic_values",
                        "dynamic_values__field",
                    )
                    .get(
                        pk=target_user_id,
                    )
                )

                fresh_actor = None

                if actor_id:
                    fresh_actor = (
                        User.objects
                        .filter(
                            pk=actor_id,
                        )
                        .first()
                    )

                logger.info(
                    "Starting user notification: "
                    "user_id=%s created=%s "
                    "changes=%r password_changed=%s",
                    target_user_id,
                    created,
                    changes,
                    password_changed,
                )

                result = (
                    UserNotificationService
                    .process(
                        target_user=(
                            fresh_target_user
                        ),
                        created=created,
                        changes=changes,
                        actor=fresh_actor,
                        password_changed=(
                            password_changed
                        ),
                    )
                )

                logger.info(
                    "User notification processed: "
                    "user_id=%s result=%r",
                    target_user_id,
                    result,
                )

            except User.DoesNotExist:
                logger.warning(
                    "User notification skipped: "
                    "user_id=%s does not exist",
                    target_user_id,
                )

            except Exception:
                logger.exception(
                    "User notification failed: "
                    "user_id=%s",
                    target_user_id,
                )

        transaction.on_commit(
            notify,
        )

        return ctx