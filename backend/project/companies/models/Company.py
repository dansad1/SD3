from django.db import models


class Company(models.Model):

    fieldset = models.ForeignKey(
        "companies.CompanyFieldSet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="companies",
    )

    archived = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-id",
        ]

    def __str__(self):

        return (
            self.get_value("name")
            or f"Company #{self.pk}"
        )

    # =====================================================
    # DYNAMIC VALUES
    # =====================================================

    def get_value(
        self,
        field_name,
    ):

        value = (
            self.dynamic_values
            .select_related("field")
            .filter(
                field__name=field_name
            )
            .first()
        )

        if not value:
            return None

        return value.value