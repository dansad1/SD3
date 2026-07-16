from backend.project.companies.models import (
    CompanyField,
)


class DepartmentFieldService:

    @staticmethod
    def get_fields(
        request,
        department=None,
    ):
        return (
            CompanyField.objects
            .filter(
                fieldset__is_active=True,
            )
            .order_by(
                "id",
            )
        )