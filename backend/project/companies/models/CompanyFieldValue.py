from django.db import models


class CompanyFieldValue(models.Model):
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "companies.CompanyField",
        on_delete=models.CASCADE,
        related_name="values",
    )

    # =====================================================
    # TYPED VALUES
    # =====================================================

    value_string = models.TextField(
        null=True,
        blank=True,
    )

    value_number = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
    )

    value_boolean = models.BooleanField(
        null=True,
        blank=True,
    )

    value_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    value_json = models.JSONField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:

        unique_together = (
            "company",
            "field",
        )

        indexes = [

            models.Index(
                fields=[
                    "company",
                    "field",
                ]
            ),

            models.Index(
                fields=[
                    "field",
                ]
            ),
        ]

    # =====================================================
    # RUNTIME VALUE
    # =====================================================

    @property
    def value(self):

        field_type = (
            self.field.field_type
        )

        if field_type in [
            "string",
            "text",
            "richtext",
        ]:
            return self.value_string

        if field_type == "number":
            return self.value_number

        if field_type == "boolean":
            return self.value_boolean

        if field_type in [
            "date",
            "datetime",
        ]:
            return self.value_datetime

        if field_type == "json":
            return self.value_json

        return self.value_string

    @value.setter
    def value(self, value):

        field_type = (
            self.field.field_type
        )

        self.value_string = None
        self.value_number = None
        self.value_boolean = None
        self.value_datetime = None
        self.value_json = None

        if field_type in [
            "string",
            "text",
            "richtext",
        ]:
            self.value_string = value

        elif field_type == "number":
            self.value_number = value

        elif field_type == "boolean":
            self.value_boolean = value

        elif field_type in [
            "date",
            "datetime",
        ]:
            self.value_datetime = value

        elif field_type == "json":
            self.value_json = value
