import json

from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)

from backend.engine.fields.providers.registry import (
    register_relation_provider,
)

from backend.project.companies.models import (
    Company,
)

from backend.project.users.models import (
    UserField,
    UserFieldValue,
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
        )

        options = [

            {
                "value": obj.pk,
                "label": str(obj),
            }

            for obj in queryset

        ]

        options.sort(

            key=lambda item: (
                item["label"]
                or ""
            ).casefold()

        )

        return options

    # =====================================================
    # INITIAL
    # =====================================================

    def get_initial(
        self,
        field,
        request=None,
        instance=None,
    ):

        if not request:
            return None


        if not request.user.is_authenticated:
            return None


        if field.name != "company":
            return None


        company_field = (
            UserField.objects
            .filter(
                name="company",
            )
            .first()
        )


        if not company_field:
            return None


        value = (
            UserFieldValue.objects
            .filter(
                user=request.user,
                field=company_field,
            )
            .first()
        )


        if not value:
            return None


        data = value.value


        # JSONField может вернуть строку
        if isinstance(
            data,
            str,
        ):

            try:

                data = json.loads(
                    data,
                )

            except (
                ValueError,
                TypeError,
            ):

                return None


        if not isinstance(
            data,
            dict,
        ):
            return None


        company_id = data.get(
            "value",
        )


        if not company_id:
            return None


        return (
            Company.objects
            .filter(
                pk=company_id,
            )
            .first()
        )

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

        return super().validate(
            field,
            value,
            request=request,
            instance=instance,
        )

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

        return super().normalize(
            field,
            value,
            request=request,
            instance=instance,
        )

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