from django.core.exceptions import (
    ValidationError,
)
from django.db import transaction

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)
from backend.project.tickets.models import (
    TicketStatus,
    TicketStatusTransition,
)
from backend.project.users.models import (
    UserRole,
)


class SaveTicketWorkflowAction(
    BaseAction,
):
    code = "ticket.workflow.save"

    permission = (
        "ticket_status_transitions.edit"
    )

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def get_value(
        data,
        camel_name,
        snake_name,
    ):
        if camel_name in data:
            return data[camel_name]

        return data.get(
            snake_name,
        )

    @classmethod
    def normalize_change(
        cls,
        change,
    ):
        if not isinstance(
            change,
            dict,
        ):
            raise ValidationError(
                "Некорректное изменение.",
            )

        source_id = cls.get_value(
            change,
            "sourceId",
            "source_id",
        )

        target_id = cls.get_value(
            change,
            "targetId",
            "target_id",
        )

        role_id = cls.get_value(
            change,
            "roleId",
            "role_id",
        )

        enabled = change.get(
            "enabled",
        )

        if not isinstance(
            enabled,
            bool,
        ):
            raise ValidationError(
                "Поле enabled должно быть boolean.",
            )

        if source_id in (
            None,
            "",
        ):
            raise ValidationError(
                "Не передан sourceId.",
            )

        if target_id in (
            None,
            "",
        ):
            raise ValidationError(
                "Не передан targetId.",
            )

        if role_id in (
            None,
            "",
        ):
            raise ValidationError(
                "Не передан roleId.",
            )

        try:
            source_id = int(
                source_id,
            )

            target_id = int(
                target_id,
            )

            role_id = int(
                role_id,
            )

        except (
            TypeError,
            ValueError,
        ) as exception:
            raise ValidationError(
                "ID должны быть числами.",
            ) from exception

        if source_id == target_id:
            raise ValidationError(
                "Переход в тот же статус запрещён.",
            )

        return {
            "source_id":
                source_id,

            "target_id":
                target_id,

            "role_id":
                role_id,

            "enabled":
                enabled,
        }

    # =====================================================
    # RUN
    # =====================================================

    @transaction.atomic
    def run(
        self,
        request,
        payload,
        ctx,
    ):
        changes = payload.get(
            "changes",
            [],
        )

        if not isinstance(
            changes,
            list,
        ):
            raise ValidationError(
                "Ожидался список изменений.",
            )

        normalized = [
            self.normalize_change(
                change,
            )
            for change in changes
        ]

        if not normalized:
            return {
                "status":
                    "ok",

                "updated":
                    0,
            }

        status_ids = {
            change["source_id"]
            for change in normalized
        }

        status_ids.update({
            change["target_id"]
            for change in normalized
        })

        role_ids = {
            change["role_id"]
            for change in normalized
        }

        statuses = {
            status.pk: status

            for status in (
                TicketStatus.objects
                .filter(
                    pk__in=status_ids,
                )
            )
        }

        roles = {
            role.pk: role

            for role in (
                UserRole.objects
                .filter(
                    pk__in=role_ids,
                )
            )
        }

        if (
            len(statuses)
            != len(status_ids)
        ):
            raise ValidationError(
                "Один или несколько статусов не найдены.",
            )

        if (
            len(roles)
            != len(role_ids)
        ):
            raise ValidationError(
                "Одна или несколько ролей не найдены.",
            )

        updated = 0

        for change in normalized:
            source = statuses[
                change["source_id"]
            ]

            target = statuses[
                change["target_id"]
            ]

            role = roles[
                change["role_id"]
            ]

            enabled = change[
                "enabled"
            ]

            if enabled:
                transition, _ = (
                    TicketStatusTransition.objects
                    .get_or_create(
                        source=source,
                        target=target,
                    )
                )

                transition.allowed_roles.add(
                    role,
                )

                updated += 1
                continue

            transition = (
                TicketStatusTransition.objects
                .select_for_update()
                .filter(
                    source=source,
                    target=target,
                )
                .first()
            )

            if not transition:
                continue

            transition.allowed_roles.remove(
                role,
            )

            if not (
                transition
                .allowed_roles
                .exists()
            ):
                transition.delete()

            updated += 1

        return {
            "status":
                "ok",

            "updated":
                updated,
        }