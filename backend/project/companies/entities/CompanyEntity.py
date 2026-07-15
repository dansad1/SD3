# =========================================================
# COMPANY ENTITY
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.companies.entities.sync import (
    sync_company,
)
from backend.project.companies.models import (
    Company,
    CompanyField,
    CompanyFieldAccess,
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
        "company",
    ]

    search_fields = [
        "name",
        "phone",
        "email",
    ]

    filter_fields = [
        "archived",
        "company",
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
        "list": "companies.view",
        "view": "companies.view",
        "create": "companies.create",
        "edit": "companies.edit",
        "delete": "companies.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):

        return [
            "fieldset",
        ]

    def get_prefetch_related(
        self,
    ):

        return [
            "dynamic_values",
        ]

    # =====================================================
    # FIELD ACCESS
    # =====================================================

    # =====================================================
    # FIELD ACCESS
    # =====================================================

    def get_field_access_map(
            self,
            request,
            obj=None,
    ):

        if (
                not request.user.is_authenticated
                or request.user.is_superuser
        ):
            return {}

        role = getattr(
            request.user,
            "role",
            None,
        )

        if role is None:
            return {}

        cache_name = "_user_field_access_map"

        access_map = getattr(
            request,
            cache_name,
            None,
        )

        if access_map is not None:
            return access_map

        access_map = {

            access.field.name:
                access.access_level

            for access in (

                CompanyFieldAccess.objects

                .select_related(
                    "field",
                )

                .filter(
                    role=role,
                )

            )

        }

        setattr(
            request,
            cache_name,
            access_map,
        )

        return access_map

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        if obj and obj.fieldset_id:

            return (

                CompanyField.objects

                .filter(
                    fieldset=obj.fieldset,
                )

                .order_by(
                    "id",
                )

            )

        if request is None:

            return (

                CompanyField.objects

                .all()

                .order_by(
                    "id",
                )

            )

        fieldset = request.GET.get(
            "fieldset",
        )

        if not fieldset or fieldset == "default":

            return (

                CompanyField.objects

                .all()

                .order_by(
                    "id",
                )

            )

        try:

            fieldset_id = int(
                fieldset,
            )

        except (
            TypeError,
            ValueError,
        ):

            return []

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
            "value": obj.pk,
            "label": (
                obj.get_value(
                    "name",
                )
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

        if not payload.get(
            "name",
        ):

            errors["name"] = [
                "Название обязательно",
            ]

        if errors:

            raise ValidationError(
                errors,
            )

        return payload

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

        sync_company(
            ctx.instance,
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
    ):

        if schema["name"] in {
            "id",
            "created_at",
            "updated_at",
        }:

            schema["readonly"] = True

        return schema

    # =====================================================
    # FILTERS
    # =====================================================

    def apply_queryset_filters(
        self,
        request,
        qs,
    ):

        qs = super().apply_queryset_filters(
            request,
            qs,
        )

        service = request.GET.get(
            "services",
        )

        if service:

            qs = qs.filter(
                services=service,
            )

        return qs