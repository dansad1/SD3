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

    @property
    def requires_post_save(
        self,
    ):
        return True

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
            dynamic_values__value__icontains=str(
                value,
            ),
        )