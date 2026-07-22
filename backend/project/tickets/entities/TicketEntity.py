from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.tickets.models import (
    Ticket,
)
from backend.project.tickets.services.StatusTransitionService import (
    StatusTransitionService,
)
from backend.project.tickets.services.TicketAfterSaveService import (
    TicketAfterSaveService,
)
from backend.project.tickets.services.TicketAssignmentPolicy import (
    TicketAssignmentService,
)
from backend.project.tickets.services.TicketFieldAccessService import (
    TicketFieldAccessService,
)
from backend.project.tickets.services.TicketFieldService import (
    TicketFieldService,
)
from backend.project.tickets.services.TicketSchemaService import (
    TicketSchemaService,
)
from backend.project.tickets.services.TicketScopeService import (
    TicketScopeService,
)


class TicketEntity(
    BaseEntity,
):
    scoped_permissions = True

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

    def apply_user_scope(
        self,
        request,
        qs,
    ):
        """
        Scope списка и открытия заявки.

        Для списка используется тот же уровень, что для view.
        """

        return TicketScopeService.apply_queryset_scope(
            entity=self,
            queryset=qs,
            user=request.user,
            action="view",
        )

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

        self.validate_scope(
            request=request,
            payload=payload,
            instance=instance,
        )

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

    # =====================================================
    # VALIDATION: SCOPE
    # =====================================================

    def validate_scope(
        self,
        request,
        payload,
        instance=None,
    ):
        if instance is None:
            TicketScopeService.validate_create(
                entity=self,
                user=request.user,
                payload=payload,
            )
            return

        TicketScopeService.check_object_access(
            entity=self,
            user=request.user,
            ticket=instance,
            action="edit",
        )

    # =====================================================
    # VALIDATION: TYPE
    # =====================================================

    def validate_type(
        self,
        payload,
        instance=None,
    ):
        ticket_type = payload.get(
            "type",
        )

        if ticket_type:
            return

        if (
            instance
            and instance.type_id
        ):
            return

        raise ValidationError({
            "type": [
                "Тип заявки обязателен.",
            ],
        })

    # =====================================================
    # VALIDATION: ASSIGNMENT
    # =====================================================

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

    # =====================================================
    # VALIDATION: STATUS
    # =====================================================

    def validate_status_transition(
        self,
        request,
        payload,
        instance=None,
    ):
        if "status" in payload:
            new_status = payload.get(
                "status",
            )
        elif instance is not None:
            new_status = instance.get_value(
                "status",
            )
        else:
            new_status = None

        if new_status is None:
            raise ValidationError({
                "status": [
                    "Статус заявки обязателен.",
                ],
            })

        old_status = (
            instance.get_value(
                "status",
            )
            if instance is not None
            else None
        )

        role = getattr(
            request.user,
            "role",
            None,
        )

        StatusTransitionService.validate_change(
            ticket=instance,
            old_status=old_status,
            new_status=new_status,
            role=role,
            comment=payload.get(
                "comment",
            ),
        )

    # =====================================================
    # DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):
        TicketScopeService.check_object_access(
            entity=self,
            user=request.user,
            ticket=instance,
            action="delete",
        )

        return super().before_delete(
            request=request,
            instance=instance,
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
        obj=None,
    ):
        return TicketSchemaService.customize(
            request=request,
            schema=schema,
            ticket=obj,
        )

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