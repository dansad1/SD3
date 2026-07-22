from backend.project.tickets.models import (
    TicketStatus,
)
from backend.project.tickets.services.StatusTransitionService import (
    StatusTransitionService,
)


class TicketSchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
        "due_date",
    }

    EDITABLE_WHEN_BLOCKED = {
        "status",
    }

    SPECIAL_FIELDS = {
        "lifecycle": {
            "widget": "timeline",
            "label": "Жизненный цикл",
        },
    }

    # =====================================================
    # CUSTOMIZE
    # =====================================================

    @classmethod
    def customize(
        cls,
        request,
        schema,
        ticket=None,
    ):
        name = schema.get(
            "name",
        )

        special = cls.SPECIAL_FIELDS.get(
            name,
        )

        if special:
            schema.update(
                special,
            )

        if name in cls.READONLY_FIELDS:
            schema["readonly"] = True

        if (
            ticket is not None
            and name not in cls.EDITABLE_WHEN_BLOCKED
            and StatusTransitionService.blocks_editing(
                ticket,
            )
        ):
            schema["readonly"] = True

        if name == "status":
            cls.customize_status(
                request=request,
                schema=schema,
                ticket=ticket,
            )

        return schema

    # =====================================================
    # STATUS
    # =====================================================

    @classmethod
    def customize_status(
        cls,
        request,
        schema,
        ticket=None,
    ):
        cls.block_empty_status(
            schema=schema,
        )

        if ticket is None:
            cls.customize_create_status(
                schema=schema,
            )
            return

        current_status = ticket.get_value(
            "status",
        )

        if current_status is None:
            cls.customize_missing_status(
                schema=schema,
            )
            return

        role = getattr(
            request.user,
            "role",
            None,
        )

        status_ids = (
            StatusTransitionService
            .get_available_statuses(
                status=current_status,
                role=role,
            )
        )

        statuses = (
            TicketStatus.objects
            .filter(
                pk__in=status_ids,
            )
            .order_by(
                "name",
                "pk",
            )
        )

        schema["options"] = [
            cls.serialize_status_option(
                status,
            )
            for status in statuses
        ]

        schema["readonly"] = not any(
            status_id != current_status.pk
            for status_id in status_ids
        )

    # =====================================================
    # EMPTY VALUE
    # =====================================================

    @classmethod
    def block_empty_status(
        cls,
        schema,
    ):
        schema["required"] = True
        schema["clearable"] = False
        schema["allow_empty"] = False
        schema["nullable"] = False

        schema["placeholder"] = ""

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def customize_create_status(
        cls,
        schema,
    ):
        statuses = cls.get_statuses()

        schema["options"] = [
            cls.serialize_status_option(
                status,
            )
            for status in statuses
        ]

        schema["readonly"] = False

    # =====================================================
    # LEGACY EMPTY STATUS
    # =====================================================

    @classmethod
    def customize_missing_status(
        cls,
        schema,
    ):
        """
        Старую заявку с пустым статусом разрешаем исправить.

        Оставить статус пустым сервер всё равно не позволит.
        """

        statuses = cls.get_statuses()

        schema["options"] = [
            cls.serialize_status_option(
                status,
            )
            for status in statuses
        ]

        schema["readonly"] = False

    # =====================================================
    # QUERYSET
    # =====================================================

    @classmethod
    def get_statuses(
        cls,
    ):
        return (
            TicketStatus.objects
            .all()
            .order_by(
                "name",
                "pk",
            )
        )

    # =====================================================
    # SERIALIZATION
    # =====================================================

    @classmethod
    def serialize_status_option(
        cls,
        status,
    ):
        return {
            "value": status.pk,
            "label": str(status),
            "color": getattr(
                status,
                "color",
                None,
            ),
        }