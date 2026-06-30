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
        ):
            return queryset

        if isinstance(
            value,
            list,
        ):
            return queryset.filter(
                dynamic_values__field_name=self.name,
                dynamic_values__value__in=[
                    str(item)
                    for item in value
                ],
            )

        return queryset.filter(
            dynamic_values__field_name=self.name,
            dynamic_values__value=str(value),
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
            dynamic_values__field_name=self.name,
            dynamic_values__value__icontains=value,
        )