from django.db import models

from backend.engine.fields.base import (
    BaseField,
)

from backend.engine.fields.django_accessor import (
    DjangoFieldAccessor,
)


class DjangoField(BaseField):

    # =====================================================
    # ACCESSOR
    # =====================================================

    @property
    def accessor(self):

        field_type_accessor = getattr(
            self.field_type,
            "accessor",
            None,
        )

        if field_type_accessor:
            return field_type_accessor

        return DjangoFieldAccessor()

    # =====================================================
    # VALUE API
    # =====================================================

    def get_value(
        self,
        obj,
    ):
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
            models.TextField,
        ):
            return "text"

        if isinstance(
            field,
            models.EmailField,
        ):
            return "email"

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

        if isinstance(
            field,
            models.BooleanField,
        ):
            return "boolean"

        if isinstance(
            field,
            models.DateTimeField,
        ):
            return "datetime"

        if isinstance(
            field,
            models.DateField,
        ):
            return "date"

        if isinstance(
            field,
            models.JSONField,
        ):
            return "json"

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