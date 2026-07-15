from backend.project.companies.models import (
    CompanyField,
)


class CompanyFieldService:

    @classmethod
    def get_fields(
        cls,
        request,
        company=None,
    ):

        if (
            company
            and company.fieldset_id
        ):

            return (

                CompanyField.objects

                .filter(
                    fieldset=company.fieldset,
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

        try:

            fieldset = int(
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
                fieldset_id=fieldset,
                fieldset__is_active=True,
            )

            .order_by(
                "id",
            )

        )