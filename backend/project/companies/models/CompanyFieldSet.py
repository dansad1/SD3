from backend.generic.models import (
    BaseFieldSet,
)


class CompanyFieldSet(
    BaseFieldSet
):

    class Meta:

        verbose_name = (
            "Company fieldset"
        )

        verbose_name_plural = (
            "Company fieldsets"
        )