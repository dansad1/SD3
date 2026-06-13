from django.db import models

from backend.engine.fields.base import BaseField
from backend.engine.fields.django_accessor import (
    DjangoFieldAccessor,
)


class DjangoField(BaseField):

    @property
    def accessor(self):
        return DjangoFieldAccessor()

    # =====================================================
    # VALUE API
    # =====================================================

    def get_value(self, obj):
        return self.accessor.get(
            obj,
            self,
        )

    def set_value(
        self,
        obj,
        value,
    ):
        return self.accessor.set(
            obj,
            self,
            value,
        )

    # =====================================================
    # CORE
    # =====================================================

    @property
    def name(self):
        return self.source.name

    @property
    def type(self):

        field = self.source

        TYPE_MAP = {
            models.TextField: "text",
            models.EmailField: "email",
            models.BooleanField: "boolean",
            models.DateTimeField: "datetime",
            models.DateField: "date",
            models.JSONField: "json",
        }

        if (
            field.name == "password"
            and isinstance(
                field,
                models.CharField,
            )
        ):
            return "password"

        if isinstance(
            field,
            (
                models.ForeignKey,
                models.ManyToManyField,
            ),
        ):
            return "relation"

        if isinstance(
            field,
            (
                models.CharField,
                models.SlugField,
            ),
        ):
            return "string"

        if isinstance(
            field,
            (
                models.IntegerField,
                models.FloatField,
                models.DecimalField,
            ),
        ):
            return "number"

        for cls, code in TYPE_MAP.items():
            if isinstance(field, cls):
                return code

        return "string"

    # =====================================================
    # META
    # =====================================================

    @property
    def label(self):
        return (
            self.source.verbose_name
            or self.name
        )

    @property
    def help_text(self):
        return (
            self.source.help_text
            or ""
        )

    @property
    def placeholder(self):
        return ""

    # =====================================================
    # VALIDATION
    # =====================================================

    @property
    def required(self):
        return not (
            self.source.blank
            or self.source.null
        )

    @property
    def unique(self):
        return getattr(
            self.source,
            "unique",
            False,
        )

    # =====================================================
    # RELATIONS
    # =====================================================

    @property
    def is_multiple(self):
        return getattr(
            self.source,
            "many_to_many",
            False,
        )

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):

        choices = getattr(
            self.source,
            "choices",
            None,
        )

        if not choices:
            return []

        return [
            {
                "value": value,
                "label": str(label),
            }
            for value, label in choices
        ]

    # =====================================================
    # OPTIONALS
    # =====================================================

    @property
    def section(self):
        return None

    @property
    def options(self):
        return {}