from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.project.companies.models import (
    Company,
    CompanyField,
)


class CompanyEntity(BaseEntity):

    model = Company

    entity = "company"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "fieldset",
        "archived",
        "created_at",
    ]

    search_fields = [
        "id",
    ]

    filter_fields = [
        "fieldset",
        "archived",
    ]

    ordering = [
        "-id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "companies.view",

        "view":
            "companies.view",

        "create":
            "companies.create",

        "edit":
            "companies.edit",

        "delete":
            "companies.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "fieldset",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        # =============================================
        # INSTANCE FIELDSET
        # =============================================

        if obj and obj.fieldset_id:

            return (
                CompanyField.objects
                .filter(
                    fieldset=obj.fieldset,
                    fieldset__is_active=True,
                )
                .order_by(
                    "order",
                    "id",
                )
            )

        # =============================================
        # QUERY FIELDSET
        # =============================================

        fieldset = request.GET.get(
            "fieldset"
        )

        if fieldset:

            try:

                fieldset = int(
                    fieldset
                )

            except (
                TypeError,
                ValueError,
            ):

                return []

            return (
                CompanyField.objects
                .filter(
                    fieldset_id=fieldset,
                    fieldset__is_active=True,
                )
                .order_by(
                    "order",
                    "id",
                )
            )

        # =============================================
        # DEFAULT
        # =============================================

        default_fieldset = (
            self.model.fieldset.field
            .model.objects
            .filter(
                is_default=True,
                is_active=True,
            )
            .first()
        )

        if not default_fieldset:
            return []

        return (
            CompanyField.objects
            .filter(
                fieldset=default_fieldset
            )
            .order_by(
                "order",
                "id",
            )
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,
            "label": str(obj),
        }