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