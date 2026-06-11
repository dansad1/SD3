from backend.engine.fields.base import (
    BaseField,
)

from backend.engine.fields.dynamic_accessor import (
    DynamicValueAccessor,
)


class DynamicField(BaseField):

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

        return DynamicValueAccessor()

    # =====================================================
    # VALUE MODEL
    # =====================================================

    @property
    def value_model(self):

        return getattr(
            self.source,
            "value_model",
            None,
        )

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
        return self.source.field_type

