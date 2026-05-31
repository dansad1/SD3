# =========================================================
# COMPANY ENTITY
# =========================================================

from django.core.exceptions import (
    ValidationError
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.project.companies.models import (
    Company,
    CompanyField,
)


class CompanyEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = Company

    entity = "company"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        # static
        "id",
        "fieldset",
        "archived",
        "created_at",

        # dynamic
        "name",
        "phone",
        "email",
    ]

    search_fields = [
        "name",
        "phone",
        "email",
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

    def get_prefetch_related(self):

        return [
            "dynamic_values",
            "dynamic_values__field",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        fieldset = request.GET.get(
            "fieldset"
        )

        # =============================================
        # DEFAULT / EMPTY
        # =============================================

        if (
            not fieldset
            or fieldset == "default"
        ):

            return (
                CompanyField.objects
                .order_by(
                    "id",
                )
            )

        # =============================================
        # VALIDATION
        # =============================================

        try:

            fieldset_id = int(
                fieldset
            )

        except (
            TypeError,
            ValueError,
        ):

            return []

        # =============================================
        # RESULT
        # =============================================

        return (
            CompanyField.objects
            .filter(
                fieldset_id=fieldset_id,
                fieldset__is_active=True,
            )
            .order_by(
                "id",
            )
        )

    # =====================================================
    # FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
        obj=None,
    ):

        fields = super().get_fields(
            request=request,
            obj=obj,
        )

        fields.extend(
            self.get_dynamic_fields(
                request=request,
                obj=obj,
            )
        )

        return fields

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,

            "label": (
                obj.get_value("name")
                or f"Company #{obj.pk}"
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

        name = payload.get(
            "name"
        )

        if not name:

            errors["name"] = [
                "Название обязательно"
            ]

        if errors:

            raise ValidationError(
                errors
            )

        return payload

    # =====================================================
    # BEFORE SAVE
    # =====================================================

    def before_save(
        self,
        ctx,
    ):

        return ctx

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
        self,
        ctx,
    ):

        return ctx

    # =====================================================
    # BEFORE DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        return None

    # =====================================================
    # AFTER DELETE
    # =====================================================

    def after_delete(
        self,
        request,
        instance,
    ):

        return None

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
        }:

            schema["readonly"] = True

        return schema