from django.core.exceptions import ValidationError

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.generic.models import (
    DynamicField,
    DjangoField,
)

from backend.project.tickets.models import (
    Ticket,
    TicketField,
    TicketFieldSet,
)

from backend.project.tickets.services.TicketAssignmentValidator import (
    TicketAssignmentValidator,
)

from backend.project.tickets.services.TicketLifecycleService import (
    TicketLifecycleService,
)

from backend.project.tickets.services.TicketSLAService import (
    TicketSLAService,
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
        "deadline",
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
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):

        return [
            "type",

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
    # FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
        obj=None,
    ):

        fields = super().get_fields(
            request,
            obj=obj,
        )

        existing_names = {
            field.name
            for field in fields
        }

        for field in self.get_dynamic_fields(
            request,
            obj=obj,
        ):

            if field.name in existing_names:
                continue

            fields.append(
                DynamicField(
                    field,
                )
            )

        return fields

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        fieldset = None

        # =============================================
        # EDIT
        # =============================================

        if (
            obj
            and obj.type_id
            and obj.type
        ):

            fieldset = obj.type.fieldset

        # =============================================
        # CREATE
        # =============================================

        else:

            type_id = (
                request.GET.get(
                    "type",
                )
                if request
                else None
            )

            if not type_id:
                return []

            try:
                type_id = int(
                    type_id,
                )

            except (
                TypeError,
                ValueError,
            ):
                return []

            ticket_type = (
                Ticket
                ._meta
                .get_field("type")
                .remote_field
                .model
                .objects
                .filter(
                    pk=type_id,
                )
                .select_related(
                    "fieldset",
                )
                .first()
            )

            if ticket_type:
                fieldset = ticket_type.fieldset

        if not fieldset:
            return []

        return (
            TicketField.objects
            .filter(
                fieldset=fieldset,
            )
            .order_by(
                "id",
            )
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

        errors = {}

        if not payload.get(
            "type",
        ):

            errors["type"] = [
                "Тип заявки обязателен",
            ]

        if errors:
            raise ValidationError(
                errors,
            )

        if instance:

            TicketAssignmentValidator.validate(
                actor=request.user,
                assignee=(
                    instance.assigned_to
                ),
            )

            old_status = instance.status

            new_status = (
                payload.get("status")
            )

            if new_status:

                TicketTransitionService.validate_transition(
                    ticket=instance,
                    old_status=old_status,
                    new_status=new_status,
                )

        return payload

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

        ticket = ctx.instance

        TicketSLAService(
            ticket,
        ).recalculate()

        if getattr(
            ctx,
            "created",
            False,
        ):

            TicketLifecycleService.on_create(
                ticket,
                ctx.request.user,
            )

        else:

            TicketLifecycleService.on_update(
                ticket,
                ctx.request.user,
                getattr(
                    ctx,
                    "changes",
                    {},
                ),
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

        if schema["name"] in {
            "id",
            "created_at",
            "updated_at",
            "due_date",
        }:

            schema["readonly"] = True

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