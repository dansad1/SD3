from django.db import models
from django.db.models.fields.reverse_related import (
    ForeignObjectRel, ManyToOneRel, ManyToManyRel,
)

from backend.engine.fields.base import BaseField
from backend.engine.fields.django_accessor import (
    DjangoFieldAccessor,
)
from backend.engine.fields.types.registry import (
    resolve_django_field_type,
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
        return resolve_django_field_type(
            self.source
        )
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
                (
                        ManyToManyRel,
                        ManyToOneRel,
                ),
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