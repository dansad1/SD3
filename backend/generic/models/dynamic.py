from django.db.models import Q

from backend.engine.fields.base import BaseField
from backend.engine.fields.dynamic_accessor import (
    DynamicValueAccessor,
)


class DynamicField(BaseField):

    @property
    def accessor(self):
        return DynamicValueAccessor()

    @property
    def value_model(self):
        return getattr(
            self.source,
            "value_model",
            None,
        )

    @property
    def name(self):
        return self.source.name

    @property
    def type(self):
        return self.source.field_type

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        value,
    ):

        if value in (
            None,
            "",
            [],
        ):
            return queryset

        filters = {
            "dynamic_values__field__name": self.name,
        }

        if isinstance(
            value,
            list,
        ):
            filters[
                "dynamic_values__value__in"
            ] = [
                str(item)
                for item in value
            ]
        else:
            filters[
                "dynamic_values__value"
            ] = str(value)

        return (
            queryset
            .filter(**filters)
            .distinct()
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def build_search_q(
        self,
        value,
    ):

        if (
            not value
            or not self.field_type.searchable
        ):
            return Q()

        return Q(
            dynamic_values__field__name=self.name,
            dynamic_values__value__icontains=str(value),
        )