from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.services.models import (
    CategoryAssignmentRule,
)

from backend.project.services.services.CategoryAssignmentRuleSchemaService import (
    CategoryAssignmentRuleSchemaService,
)
from backend.project.services.services.CategoryAssignmentRuleValidationService import (
    CategoryAssignmentRuleValidationService,
)


class CategoryAssignmentRuleEntity(BaseEntity):

    model = CategoryAssignmentRule

    entity = "category_assignment_rule"

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

    capabilities = {
        "list": "services.view",
        "view": "services.view",
        "create": "services.edit",
        "edit": "services.edit",
        "delete": "services.edit",
    }

    def get_select_related(
        self,
    ):
        return [
            "service",
            "category",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "executors",
            "executor_groups",
            "watchers",
        ]

    def represent_option(
        self,
        obj,
    ):
        return {
            "value": obj.pk,
            "label": (
                f"{obj.service} → "
                f"{obj.category}"
            ),
        }

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        return (
            CategoryAssignmentRuleValidationService
            .validate(
                payload=payload,
                instance=instance,
            )
        )

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):
        return (
            CategoryAssignmentRuleSchemaService
            .customize(
                request=request,
                schema=schema,
                field=field,
            )
        )