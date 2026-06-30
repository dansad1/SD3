from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)

from backend.engine.fields.providers.registry import (
    register_relation_provider,
)

from backend.project.companies.models import (
    Company,
)


@register_relation_provider
class CompanyProvider(
    BaseRelationProvider,
):

    code = "company"

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):

        queryset = (
            Company.objects
            .all()
            .order_by(
                "name",
            )
        )

        return [
            {
                "value": obj.pk,
                "label": str(obj),
            }
            for obj in queryset
        ]

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        value = super().validate(
            field,
            value,
            request=request,
            instance=instance,
        )

        return value

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def normalize(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        value = super().normalize(
            field,
            value,
            request=request,
            instance=instance,
        )

        return value

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def serialize(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        return super().serialize(
            field,
            value,
            request=request,
            instance=instance,
        )

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        return super().apply_filter(
            queryset,
            field,
            value,
        )

    # =====================================================
    # BEFORE SAVE
    # =====================================================

    def before_save(
        self,
        instance,
        field,
        value,
    ):

        pass

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
        self,
        instance,
        field,
        value,
    ):

        pass