class BaseField:

    META_FIELDS = {
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by",
        "updated_by",
    }

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
    # PRESENTATION
    # =====================================================

    @property
    def presentation(self):

        if self.name in self.META_FIELDS:
            return "meta"

        return None

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
            "",
        )

    @property
    def help_text(self):
        return getattr(
            self.source,
            "help_text",
            "",
        )

    @property
    def section(self):
        return getattr(
            self.source,
            "section",
            None,
        )

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):
        return getattr(
            self.source,
            "choices",
            [],
        ) or []

    # =====================================================
    # OPTIONS
    # =====================================================

    @property
    def options(self):

        value = getattr(
            self.source,
            "options",
            None,
        )

        return value or {}

    # =====================================================
    # TYPE
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

    def should_save(
            self,
            value,
    ):
        return (
            self.field_type
            .should_save(
                self,
                value,
            )
        )
    def serialize(self, value):
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
    # SCHEMA
    # =====================================================

    def get_schema(self):

        schema = self.field_type.get_schema(
            self
        )

        schema.update({
            "name": self.name,
            "label": self.label,

            "required": self.required,
            "placeholder": self.placeholder,
            "help_text": self.help_text,

            "multiple": self.is_multiple,
            "unique": self.unique,
        })

        if self.presentation:
            schema["presentation"] = (
                self.presentation
            )

        if self.section:

            schema.setdefault(
                "ui",
                {}
            )

            schema["ui"]["section"] = (
                self.section
            )

        if (
            "options" not in schema
            and self.choices
        ):
            schema["options"] = (
                self.choices
            )

        return schema

    # =====================================================
    # FILTER / SEARCH
    # =====================================================

    def apply_filter(

            self,

            queryset,

            value,

    ):

        print(

            "CALL",

            self.name,

            value,

        )

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

    def build_search_q(
            self,
            value,
    ):

        return self.field_type.build_search_q(
            self,
            value,
        )