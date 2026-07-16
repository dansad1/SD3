from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.services.models import (
    WorkSchedule,
)

from backend.project.services.services.WorkScheduleSchemaService import (
    WorkScheduleSchemaService,
)
from backend.project.services.services.WorkScheduleValidationService import (
    WorkScheduleValidationService,
)


class WorkScheduleEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = WorkSchedule

    entity = "schedule"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "name",
        "owner",
        "days",
        "start_time",
        "end_time",
        "created_at",
    ]

    search_fields = [
        "name",
    ]

    filter_fields = [
        "owner",
        "days",
        "archived",
    ]

    ordering = [
        "name",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "services.view",
        "view": "services.view",
        "create": "services.edit",
        "edit": "services.edit",
        "delete": "services.edit",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):
        return [
            "owner",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "days",
        ]

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):
        return {
            "value": obj.pk,
            "label": obj.name,
        }

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        return (
            WorkScheduleValidationService
            .validate(
                payload=payload,
                instance=instance,
            )
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):
        return (
            WorkScheduleSchemaService
            .customize(
                request=request,
                schema=schema,
                field=field,
            )
        )