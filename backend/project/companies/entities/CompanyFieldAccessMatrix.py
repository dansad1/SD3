from backend.project.audit.utils.BaseFieldAccessMatrix import BaseFieldAccessMatrix
from backend.project.companies.models import (
    CompanyField,
    CompanyFieldAccess,
)


class CompanyFieldAccessMatrix(
    BaseFieldAccessMatrix,
):

    field_model = CompanyField

    access_model = CompanyFieldAccess

    role_order = "id"

    class Meta:

        code = "company-field.access"

        capabilities = {
            "view": "company_fields.edit",
            "edit": "company_fields.edit",
        }