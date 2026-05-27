# =========================================================
# backend/project/services/entities/WorkScheduleEntity.py
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.services.models import (
    WorkSchedule,
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

        "list":
            "services.view",

        "view":
            "services.view",

        "create":
            "services.edit",

        "edit":
            "services.edit",

        "delete":
            "services.edit",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [

            "owner",
        ]

    def get_prefetch_related(self):

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

            "value":
                obj.pk,

            "label":
                obj.name,
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

        errors = {}

        # =================================================
        # NAME
        # =================================================

        if not payload.get(
            "name"
        ):

            errors["name"] = [
                "Название обязательно"
            ]

        # =================================================
        # TIME
        # =================================================

        start_time = payload.get(
            "start_time"
        )

        end_time = payload.get(
            "end_time"
        )

        if (

            start_time
            and end_time
            and start_time >= end_time

        ):

            errors["end_time"] = [

                "Время окончания должно быть больше времени начала"

            ]

        # =================================================
        # RESULT
        # =================================================

        if errors:

            raise ValidationError(
                errors
            )

        return payload

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):

        # =================================================
        # READONLY
        # =================================================

        if schema["name"] in {

            "id",

            "created_at",

            "updated_at",
        }:

            schema["readonly"] = True

        # =================================================
        # OWNER
        # =================================================

        if schema["name"] == "owner":

            schema["widget"] = (
                "entity_select"
            )

            schema["entity"] = (
                "user"
            )

        # =================================================
        # DAYS
        # =================================================

        if schema["name"] == "days":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = (
                "day_of_week"
            )

        return schema