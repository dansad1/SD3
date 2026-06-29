from django.contrib.contenttypes.fields import (
    GenericRelation,
)
from django.db import models

from backend.generic.models import (
    DynamicValue,
)


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

    dynamic_values = GenericRelation(
        DynamicValue,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="company",
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

    def get_dynamic_map(
        self,
    ):

        if hasattr(
            self,
            "_dynamic_map",
        ):
            return self._dynamic_map

        values = {}

        for item in self.dynamic_values.all():

            values[
                item.field_name
            ] = item.value

        self._dynamic_map = values

        return values

    # =====================================================
    # VALUE
    # =====================================================

    def get_value(
        self,
        field_name,
    ):

        return (
            self.get_dynamic_map()
            .get(field_name)
        )