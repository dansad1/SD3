from django.db import models
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
)

from backend.engine.fields.base import BaseField
from backend.engine.fields.django_accessor import (
    DjangoFieldAccessor,
)
from backend.engine.fields.types.RelationAccessor import (
    RelationAccessor,
)


class DjangoField(BaseField):

    # =====================================================
    # ACCESSOR
    # =====================================================

    @property
    def accessor(self):

        if self.type == "relation":
            return RelationAccessor()

        return DjangoFieldAccessor()

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        value,
    ):
        return self.field_type.apply_filter(
            queryset,
            self,
            value,
        )

    # =====================================================
    # VALUE
    # =====================================================

    @property
    def name(self):
        return self.source.name

    @property
    def type(self):

        field = self.source

        # ==========================================
        # SPECIAL
        # ==========================================

        if (
                field.name == "password"
                and isinstance(
            field,
            models.CharField,
        )
        ):
            return "password"

        # ==========================================
        # FILES
        # ==========================================

        if isinstance(
                field,
                (
                        models.FileField,
                        models.ImageField,
                ),
        ):
            return "file"

        # ==========================================
        # RELATIONS
        # ==========================================

        if isinstance(
                field,
                (
                        models.ForeignKey,
                        models.OneToOneField,
                        models.ManyToManyField,
                        ForeignObjectRel,
                ),
        ):
            return "relation"

        # ==========================================
        # TEXT
        # ==========================================

        if isinstance(
                field,
                (
                        models.CharField,
                        models.SlugField,
                        models.URLField,
                        models.UUIDField,
                ),
        ):
            return "string"

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

        # ==========================================
        # NUMBERS
        # ==========================================

        if isinstance(
                field,
                (
                        models.SmallIntegerField,
                        models.IntegerField,
                        models.BigIntegerField,
                        models.PositiveIntegerField,
                        models.PositiveSmallIntegerField,
                        models.FloatField,
                        models.DecimalField,
                ),
        ):
            return "number"

        # ==========================================
        # BOOLEAN
        # ==========================================

        if isinstance(
                field,
                models.BooleanField,
        ):
            return "boolean"

        # ==========================================
        # DATE
        # ==========================================

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

        # ==========================================
        # JSON
        # ==========================================

        if isinstance(
                field,
                models.JSONField,
        ):
            return "json"

        # ==========================================
        # FALLBACK
        # ==========================================

        return "string"
    # =====================================================
    # META
    # =====================================================

    @property
    def label(self):
        return (
            getattr(
                self.source,
                "verbose_name",
                None,
            )
            or self.name
        )

    @property
    def help_text(self):
        return (
            getattr(
                self.source,
                "help_text",
                "",
            )
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

        if isinstance(
            self.source,
            ForeignObjectRel,
        ):
            return False

        return not (
            getattr(
                self.source,
                "blank",
                False,
            )
            or getattr(
                self.source,
                "null",
                False,
            )
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

        if isinstance(
            self.source,
            ForeignObjectRel,
        ):
            return True

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