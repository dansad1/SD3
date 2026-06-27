from backend.engine.fields.base import (
    BaseField,
)

from backend.engine.fields.dynamic_accessor import (
    DynamicValueAccessor,
)


class DynamicField(
    BaseField,
):

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
    # VALUE
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

            values = [
                str(item)
                for item in value
            ]

            return queryset.filter(
                dynamic_values__field_name=self.name,
                dynamic_values__value__in=values,
            )

        return queryset.filter(
            dynamic_values__field_name=self.name,
            dynamic_values__value=str(value),
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def apply_search(
        self,
        queryset,
        value,
    ):

        if not value:
            return queryset

        return queryset.filter(
            dynamic_values__field_name=self.name,
            dynamic_values__value__icontains=value,
        )