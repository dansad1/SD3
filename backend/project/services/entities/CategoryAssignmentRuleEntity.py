# =========================================================
# backend/project/services/entities/CategoryAssignmentRuleEntity.py
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.services.models import (
    CategoryAssignmentRule,
)


class CategoryAssignmentRuleEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = CategoryAssignmentRule

    entity = "category_assignment_rule"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "id",

        "service",

        "category",

        "executors",

        "executor_groups",

        "watchers",
    ]

    search_fields = []

    filter_fields = [

        "service",

        "category",
    ]

    ordering = [

        "service",

        "category",
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

            "service",

            "category",
        ]

    def get_prefetch_related(self):

        return [

            "executors",

            "executor_groups",

            "watchers",
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
                (
                    f"{obj.service} → "
                    f"{obj.category}"
                ),
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
        # REQUIRED
        # =================================================

        service = payload.get(
            "service"
        )

        category = payload.get(
            "category"
        )

        if not service:

            errors["service"] = [
                "Сервис обязателен"
            ]

        if not category:

            errors["category"] = [
                "Категория обязательна"
            ]

        # =================================================
        # UNIQUE
        # =================================================

        if service and category:

            qs = (
                CategoryAssignmentRule.objects
                .filter(
                    service=service,
                    category=category,
                )
            )

            if instance:

                qs = qs.exclude(
                    pk=instance.pk
                )

            if qs.exists():

                errors["category"] = [

                    "Правило для этой категории уже существует"

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

        if schema["name"] == "id":

            schema["readonly"] = True

        # =================================================
        # SERVICE
        # =================================================

        if schema["name"] == "service":

            schema["widget"] = (
                "entity_select"
            )

            schema["entity"] = (
                "service"
            )

        # =================================================
        # CATEGORY
        # =================================================

        if schema["name"] == "category":

            schema["widget"] = (
                "entity_select"
            )

            schema["entity"] = (
                "ticket_category"
            )

        # =================================================
        # EXECUTORS
        # =================================================

        if schema["name"] == "executors":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = (
                "user"
            )

        # =================================================
        # GROUPS
        # =================================================

        if schema["name"] == "executor_groups":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = (
                "executor_group"
            )

        # =================================================
        # WATCHERS
        # =================================================

        if schema["name"] == "watchers":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = (
                "user"
            )

        return schema