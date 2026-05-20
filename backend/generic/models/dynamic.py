from backend.engine.fields.base import (
    BaseField,
)
from backend.engine.fields.dynamic_accessor import DynamicValueAccessor


class DynamicField(BaseField):

    # =====================================================
    # ACCESSOR
    # =====================================================

    @property
    def accessor(self):

        return DynamicValueAccessor()

    # =====================================================
    # VALUE MODEL
    # =====================================================

    @property
    def value_model(self):

        # 🔥 overridable
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

    # =====================================================
    # UI
    # =====================================================

    @property
    def label(self):

        return (
            self.source.label
            or self.name
        )

    @property
    def placeholder(self):

        return self.source.placeholder

    @property
    def help_text(self):

        return self.source.help_text

    @property
    def widget(self):

        return self.source.widget

    @property
    def width(self):

        return self.source.width

    @property
    def order(self):

        return self.source.order

    # =====================================================
    # VALIDATION
    # =====================================================

    @property
    def required(self):

        return self.source.required

    @property
    def readonly(self):

        return self.source.readonly

    @property
    def hidden(self):

        return self.source.hidden

    @property
    def unique(self):

        return self.source.unique

    @property
    def regex(self):

        return self.source.regex

    @property
    def min_value(self):

        return self.source.min_value

    @property
    def max_value(self):

        return self.source.max_value

    # =====================================================
    # RELATIONS
    # =====================================================

    @property
    def is_multiple(self):

        return self.source.is_multiple

    @property
    def relation_entity(self):

        return (
            self.source.relation_entity
        )

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):

        return (
            self.source.choices
            or []
        )