from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.project.companies.models import (
    CompanyField
)


class CompanyFieldEntity(BaseEntity):

    model = CompanyField

    entity = "company-fields"

    list_display = [
        "fieldset",
        "name",
        "label",
        "field_type",
        "required",
        "readonly",
        "hidden",
        "order",
    ]

    search_fields = [
        "name",
        "label",
    ]

    filter_fields = [
        "fieldset",
        "field_type",
    ]

    ordering = [
        "fieldset",
        "order",
        "id",
    ]

    capabilities = {
        "list": "company_fields.view",
        "view": "company_fields.view",
        "create": "company_fields.create",
        "edit": "company_fields.edit",
        "delete": "company_fields.delete",
    }

    def get_select_related(self):

        return [
            "fieldset",
        ]