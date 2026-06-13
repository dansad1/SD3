from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.companies.models import (
    CompanyField,
)


class CompanyFieldEntity(BaseEntity):

    model = CompanyField

    entity = "company-fields"

    exclude_fields = [

        "fieldset",
    ]

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "name",

        "label",

        "field_type",

        "required",

        "unique",

        "is_multiple",

        "is_system",
    ]

    search_fields = [

        "name",

        "label",
    ]

    filter_fields = [

        "field_type",
    ]

    ordering = [

        "id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list": "company_fields.view",

        "view": "company_fields.view",

        "create": "company_fields.create",

        "edit": "company_fields.edit",

        "delete": "company_fields.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "fieldset",
        ]