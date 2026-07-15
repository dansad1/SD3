from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.tickets.models import (
    Ticket,
)
from backend.project.tickets.services.TicketAfterSaveService import (
    TicketAfterSaveService,
)
from backend.project.tickets.services.TicketAssignmentPolicy import TicketAssignmentService

from backend.project.tickets.services.TicketFieldAccessService import (
    TicketFieldAccessService,
)
from backend.project.tickets.services.TicketFieldService import (
    TicketFieldService,
)
from backend.project.tickets.services.TicketTransitionService import (
    TicketTransitionService,
)


class TicketEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = Ticket

    entity = "tickets"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "type",
        "status",
        "priority",
        "company",
        "executor_group",
        "assigned_to",
        "due_date",
        "created_at",
    ]

    search_fields = [
        "id",
    ]

    filter_fields = [
        "type",
        "status",
        "priority",
        "company",
        "executor_group",
        "assigned_to",
        "archived",
    ]

    ordering = [
        "-created_at",
    ]

    exclude_fields = [
        "deleted_at",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "tickets.view",
        "view": "tickets.view",
        "create": "tickets.create",
        "edit": "tickets.edit",
        "delete": "tickets.delete",
    }

    # =====================================================
    # FIELD ACCESS
    # =====================================================

    def get_field_access_map(
        self,
        request,
        obj=None,
    ):
        return TicketFieldAccessService.get_access_map(
            request=request,
        )

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):
        return [
            "type",
            "type__fieldset",
            "status",
            "assigned_to",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "dynamic_values",
            "dynamic_values__field",
            "comments",
            "attachments",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):
        return TicketFieldService.get_fields(
            request=request,
            ticket=obj,
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        payload = payload or {}

        self.validate_type(
            payload=payload,
            instance=instance,
        )

        self.validate_assignment(
            request=request,
            payload=payload,
            instance=instance,
        )

        self.validate_status_transition(
            request=request,
            payload=payload,
            instance=instance,
        )

        return payload

    def validate_type(
        self,
        payload,
        instance=None,
    ):
        ticket_type = payload.get(
            "type",
        )

        if (
            ticket_type
            or (
                instance
                and instance.type_id
            )
        ):
            return

        raise ValidationError(
            {
                "type": [
                    "Тип заявки обязателен.",
                ],
            },
        )

    def validate_assignment(
        self,
        request,
        payload,
        instance=None,
    ):
        if "assigned_to" not in payload:
            return

        executor = payload.get(
            "assigned_to",
        )

        TicketAssignmentService.validate_executor(
            actor=request.user,
            executor=executor,
        )

    def validate_status_transition(
        self,
        request,
        payload,
        instance=None,
    ):
        if instance is None:
            return

        if "status" not in payload:
            return

        new_status = payload.get(
            "status",
        )

        if new_status is None:
            return

        role = getattr(
            request.user,
            "role",
            None,
        )

        TicketTransitionService.validate_transition(
            ticket=instance,
            old_status=instance.status,
            new_status=new_status,
            role=role,
        )

    # =====================================================
    # LIFECYCLE
    # =====================================================

    def after_save(
        self,
        ctx,
    ):
        ctx = super().after_save(
            ctx,
        )

        TicketAfterSaveService.process(
            ctx=ctx,
        )

        return ctx

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):
        field_name = schema.get(
            "name",
        )

        readonly_fields = {
            "id",
            "created_at",
            "updated_at",
            "due_date",
        }

        if field_name in readonly_fields:
            schema["readonly"] = True

        if field_name == "lifecycle":
            schema.update(
                {
                    "widget": "timeline",
                    "label": "Жизненный цикл",
                },
            )

        return schema

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_option(
        self,
        obj,
    ):
        return {
            "value": obj.pk,
            "label": str(obj),
        }