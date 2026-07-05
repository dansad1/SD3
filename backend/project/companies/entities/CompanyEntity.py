# =========================================================
# COMPANY ENTITY
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.companies.entities.sync import sync_company

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

        "id",

        "archived",

        "created_at",

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

        "archived",

    ]

    ordering = [

        "-created_at",

    ]

    exclude_fields = [

        "fieldset",

        "created_at",

        "updated_at",

        "choices",

        "options",

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

        #
        # DynamicValue не имеет FK field
        #

        return [

            "dynamic_values",

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
        # EXISTING COMPANY
        # =============================================

        if (

            obj

            and obj.fieldset_id

        ):

            return (

                CompanyField.objects

                .filter(

                    fieldset=obj.fieldset,

                )

                .order_by(

                    "id",

                )

            )

        # =============================================
        # NO REQUEST
        # =============================================

        if request is None:

            return (

                CompanyField.objects

                .all()

                .order_by(

                    "id",

                )

            )

        # =============================================
        # CREATE MODE
        # =============================================

        fieldset = (

            request.GET.get(

                "fieldset",

            )

        )

        # =============================================
        # DEFAULT
        # =============================================

        if (

            not fieldset

            or fieldset == "default"

        ):

            return (

                CompanyField.objects

                .all()

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

                    obj.get_value(

                        "name",

                    )

                    or

                    f"Company #{obj.pk}"

                )

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

        name = (

            payload.get(

                "name"

            )

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
    # LIFECYCLE
    # =====================================================

    def before_save(

        self,

        ctx,

    ):

        return ctx

    def after_save(
            self,
            ctx,
    ):
        ctx = super().after_save(
            ctx,
        )

        sync_company(
            ctx.instance,
        )

        return ctx

    def before_delete(

        self,

        request,

        instance,

    ):

        return None

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