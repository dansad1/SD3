# =========================================================
# backend/dynamic/fields/base.py
# =========================================================


class BaseField:
    """
    Runtime field abstraction.

    Это НЕ django model.
    Это runtime schema object.
    """

    def __init__(self, source):

        self.source = source

    # =====================================================
    # REQUIRED
    # =====================================================

    @property
    def name(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    # =====================================================
    # COMMON
    # =====================================================

    @property
    def label(self):

        return getattr(
            self.source,
            "label",
            self.name,
        )

    @property
    def required(self):

        return getattr(
            self.source,
            "required",
            False,
        )

    @property
    def readonly(self):

        return getattr(
            self.source,
            "readonly",
            False,
        )

    @property
    def hidden(self):

        return getattr(
            self.source,
            "hidden",
            False,
        )

    @property
    def unique(self):

        return getattr(
            self.source,
            "unique",
            False,
        )

    @property
    def is_multiple(self):

        return getattr(
            self.source,
            "is_multiple",
            False,
        )

    # =====================================================
    # UI
    # =====================================================

    @property
    def placeholder(self):

        return getattr(
            self.source,
            "placeholder",
            None,
        )

    @property
    def help_text(self):

        return getattr(
            self.source,
            "help_text",
            None,
        )

    @property
    def widget(self):

        return getattr(
            self.source,
            "widget",
            None,
        )

    @property
    def width(self):

        return getattr(
            self.source,
            "width",
            12,
        )

    @property
    def order(self):

        return getattr(
            self.source,
            "order",
            0,
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    @property
    def regex(self):

        return getattr(
            self.source,
            "regex",
            None,
        )

    @property
    def min_value(self):

        return getattr(
            self.source,
            "min_value",
            None,
        )

    @property
    def max_value(self):

        return getattr(
            self.source,
            "max_value",
            None,
        )

    # =====================================================
    # RELATION
    # =====================================================

    @property
    def relation_entity(self):

        return getattr(
            self.source,
            "relation_entity",
            None,
        )

    # =====================================================
    # DEFAULT
    # =====================================================

    @property
    def default_value(self):

        return getattr(
            self.source,
            "default_value",
            None,
        )

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):

        value = getattr(
            self.source,
            "choices",
            None,
        )

        if not value:
            return []

        return value

    # =====================================================
    # TYPE OBJECT
    # =====================================================

    @property
    def field_type(self):
        from backend.engine.fields.types.registry import (
            get_field_type,
        )

        return get_field_type(
            self.type
        )

    # =====================================================
    # BEHAVIOR
    # =====================================================

    def validate(self, value):

        return self.field_type.validate(
            self,
            value,
        )

    def normalize(self, value):

        return self.field_type.normalize(
            self,
            value,
        )

    def serialize(
            self,
            value,
    ):
        return self.field_type.serialize(
            self,
            value,
        )
    def deserialize(self, value):

        return self.field_type.deserialize(
            self,
            value,
        )

    # =====================================================
    # UI SCHEMA
    # =====================================================

    def get_schema(self):

        schema = self.field_type.get_schema(self)

        schema.update({
            "name": self.name,
            "label": self.label,
            "required": self.required,
            "readonly": self.readonly,
            "hidden": self.hidden,
            "placeholder": self.placeholder,
            "help_text": self.help_text,
            "width": self.width,
            "multiple": self.is_multiple,
        })

        # 🔥 enum support
        if self.choices:
            schema["choices"] = self.choices
            schema["widget"] = "Select"

        return schema

    # =====================================================
    # FILTER / SEARCH
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

    def apply_search(
        self,
        queryset,
        value,
    ):

        return self.field_type.apply_search(
            queryset,
            self,
            value,
        )

    # =====================================================
    # VALUE ACCESS
    # =====================================================

    def get_value(
        self,
        accessor,
        obj,
    ):

        return accessor.get(
            obj,
            self,
        )

    def set_value(
        self,
        accessor,
        obj,
        value,
    ):

        normalized = self.normalize(
            value
        )

        self.validate(
            normalized
        )

        return accessor.set(
            obj,
            self,
            normalized,
        )