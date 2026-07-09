from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.tickets.models import (
    Ticket,
    TicketField,
    TicketFieldAccess, TicketType,
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

    def get_field_access_map(
        self,
        request,
        obj=None,
    ):

        if (
            not request.user.is_authenticated
            or request.user.is_superuser
        ):
            return {}

        role = getattr(
            request.user,
            "role",
            None,
        )

        if not role:
            return {}

        return {

            item.field.name:
                item.access_level

            for item in (

                TicketFieldAccess.objects

                .select_related(
                    "field",
                )

                .filter(
                    role=role,
                )

            )

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
    # DYNAMIC FIELDS
    # =====================================================



    def get_dynamic_fields(
            self,
            request,
            obj=None,
    ):

        print("\n" + "=" * 80)
        print("TicketEntity.get_dynamic_fields()")
        print("=" * 80)

        fieldset = None

        print(
            "REQUEST.GET =",
            dict(request.GET) if request else None,
        )

        payload = getattr(
            request,
            "_form_payload",
            {},
        ) if request else {}

        print(
            "PAYLOAD =",
            payload,
        )

        # =====================================================
        # EDIT
        # =====================================================

        if obj is not None:

            print("\nMODE = EDIT")
            print("OBJECT =", obj)
            print("PK =", obj.pk)
            print("TYPE_ID =", obj.type_id)

            if obj.type_id:

                print("TYPE =", obj.type)

                fieldset = getattr(
                    obj.type,
                    "fieldset",
                    None,
                )

                print("FIELDSET =", fieldset)

            else:

                print("TYPE_ID IS NONE")

        # =====================================================
        # CREATE
        # =====================================================

        else:

            print("\nMODE = CREATE")

            type_id = None

            # ---------------------------------------------
            # PAYLOAD
            # ---------------------------------------------

            if payload:

                type_id = payload.get(
                    "type",
                )

                if hasattr(
                        type_id,
                        "pk",
                ):
                    type_id = type_id.pk

                elif isinstance(
                        type_id,
                        dict,
                ):
                    type_id = type_id.get(
                        "value",
                    )

            # ---------------------------------------------
            # QUERY
            # ---------------------------------------------

            if (
                    not type_id
                    and request
            ):
                type_id = request.GET.get(
                    "type",
                )

            print(
                "TYPE_ID =",
                type_id,
            )

            if not type_id:
                print("NO TYPE")

                print("=" * 80)

                return []

            try:

                type_id = int(
                    type_id,
                )

            except (
                    TypeError,
                    ValueError,
            ):

                print(
                    "INVALID TYPE:",
                    type_id,
                )

                print("=" * 80)

                return []

            ticket_type = (

                TicketType.objects

                .select_related(
                    "fieldset",
                )

                .filter(
                    pk=type_id,
                )

                .first()

            )

            print(
                "TICKET TYPE =",
                ticket_type,
            )

            if ticket_type:

                fieldset = (
                    ticket_type.fieldset
                )

                print(
                    "FIELDSET =",
                    fieldset,
                )

            else:

                print(
                    "TYPE NOT FOUND",
                )

        # =====================================================
        # FIELDSET
        # =====================================================

        if fieldset is None:
            print(
                "FIELDSET IS NONE",
            )

            print("=" * 80)

            return []

        # =====================================================
        # FIELDS
        # =====================================================

        fields = (

            TicketField.objects

            .filter(
                fieldset=fieldset,
            )

            .order_by(
                "id",
            )

        )

        print(
            "FIELDS COUNT =",
            fields.count(),
        )

        for field in fields:
            print(
                f"  - {field.id}: "
                f"{field.name} "
                f"({field.field_type})"
            )

        print("=" * 80)

        return fields
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
                assignee=instance.assigned_to,
            )

            new_status = payload.get(
                "status",
            )

            if new_status:

                TicketTransitionService.validate_transition(
                    ticket=instance,
                    old_status=instance.status,
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
                    [],
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