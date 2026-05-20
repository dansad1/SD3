from backend.engine.fields.base import (
    BaseField,
)


class ActionField(BaseField):

    def __init__(
        self,
        data,
    ):

        super().__init__(data)

    # =====================================================
    # REQUIRED
    # =====================================================

    @property
    def name(self):

        return self.source.get(
            "name"
        )

    @property
    def type(self):

        return self.source.get(

            "type",

            self.source.get(
                "field_type",
                "string",
            ),
        )

    # =====================================================
    # COMMON
    # =====================================================

    @property
    def label(self):

        return self.source.get(
            "label",
            self.name,
        )

    @property
    def required(self):

        return self.source.get(
            "required",
            False,
        )

    @property
    def readonly(self):

        return self.source.get(
            "readonly",
            False,
        )

    @property
    def hidden(self):

        return self.source.get(
            "hidden",
            False,
        )

    @property
    def is_multiple(self):

        return self.source.get(
            "multiple",
            False,
        )

    # =====================================================
    # UI
    # =====================================================

    @property
    def placeholder(self):

        return self.source.get(
            "placeholder"
        )

    @property
    def help_text(self):

        return self.source.get(
            "help_text"
        )

    @property
    def widget(self):

        return self.source.get(
            "widget"
        )

    @property
    def width(self):

        return self.source.get(
            "width",
            12,
        )

    @property
    def order(self):

        return self.source.get(
            "order",
            0,
        )

    # =====================================================
    # RELATION
    # =====================================================

    @property
    def relation_entity(self):

        return self.source.get(
            "relation_entity"
        )

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):

        return (
            self.source.get(
                "choices"
            )
            or []
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    @property
    def regex(self):

        return self.source.get(
            "regex"
        )

    @property
    def min_value(self):

        return self.source.get(
            "min_value"
        )

    @property
    def max_value(self):

        return self.source.get(
            "max_value"
        )