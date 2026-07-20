from backend.generic.models import (
    BaseFieldSet,
)


class CompanyFieldSet(
    BaseFieldSet,
):

    class Meta:

        verbose_name = (
            "Набор полей компании"
        )

        verbose_name_plural = (
            "Наборы полей компаний"
        )
