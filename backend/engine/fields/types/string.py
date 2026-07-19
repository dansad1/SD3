import unicodedata

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class StringFieldType(
    BaseFieldType,
):

    code = "string"

    label = "String"

    widget = "text"
    multiple_widget = None

    searchable = True
    sortable = True
    filterable = True

    features = [
        "required",
        "unique",
        "placeholder",
        "help_text",
    ]

    DEFAULT_MAX_LENGTH = 10000
    ABSOLUTE_MAX_LENGTH = 100000

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_option(
        self,
        field,
        name,
        default=None,
    ):
        options = getattr(
            field,
            "options",
            None,
        ) or {}

        return options.get(
            name,
            default,
        )

    def get_min_length(
        self,
        field,
    ):
        value = self.get_option(
            field,
            "min_length",
            0,
        )

        try:
            value = int(value)

        except (
            TypeError,
            ValueError,
        ):
            value = 0

        return max(
            value,
            0,
        )

    def get_max_length(
        self,
        field,
    ):
        source = getattr(
            field,
            "source",
            None,
        )

        source_max_length = getattr(
            source,
            "max_length",
            None,
        )

        value = self.get_option(
            field,
            "max_length",
            source_max_length,
        )

        if value is None:
            value = self.DEFAULT_MAX_LENGTH

        try:
            value = int(value)

        except (
            TypeError,
            ValueError,
        ):
            value = self.DEFAULT_MAX_LENGTH

        return min(
            max(
                value,
                1,
            ),
            self.ABSOLUTE_MAX_LENGTH,
        )

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_string(
        self,
        value,
    ):
        if not isinstance(
            value,
            (
                str,
                int,
                float,
            ),
        ):
            raise ValidationError(
                "Некорректное значение"
            )

        value = str(
            value
        )

        value = unicodedata.normalize(
            "NFKC",
            value,
        )

        value = value.strip()

        for char in value:
            if (
                ord(char) < 32
                and char not in (
                    "\n",
                    "\r",
                    "\t",
                )
            ):
                raise ValidationError(
                    "Недопустимые символы"
                )

        return value

    # =====================================================
    # LENGTH
    # =====================================================

    def validate_length(
        self,
        field,
        value,
    ):
        min_length = self.get_min_length(
            field
        )

        max_length = self.get_max_length(
            field
        )

        if (
            min_length
            and len(value) < min_length
        ):
            raise ValidationError(
                f"Минимальная длина: {min_length}"
            )

        if len(value) > max_length:
            raise ValidationError(
                f"Максимальная длина: {max_length}"
            )

        return value

    # =====================================================
    # VALUE
    # =====================================================

    def normalize_value(
        self,
        field,
        value,
    ):
        value = self.to_string(
            value
        )

        return self.validate_length(
            field,
            value,
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):
        value = super().validate(
            field,
            value,
        )

        if value in (
            None,
            "",
        ):
            return value

        if field.is_multiple:
            return [
                self.normalize_value(
                    field,
                    item,
                )
                for item in value
            ]

        return self.normalize_value(
            field,
            value,
        )

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):
        if value is None:
            return None

        if field.is_multiple:
            return [
                self.normalize_value(
                    field,
                    item,
                )
                for item in value
            ]

        return self.normalize_value(
            field,
            value,
        )

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        if value is None:
            return None

        if field.is_multiple:
            return [
                str(item)
                for item in value
            ]

        return str(
            value
        )

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):
        if value is None:
            return None

        if field.is_multiple:
            return [
                str(item)
                for item in value
            ]

        return str(
            value
        )

    # =====================================================
    # WIDGET
    # =====================================================

    def get_widget(
        self,
        field,
    ):
        explicit_widget = self.get_option(
            field,
            "widget",
        )

        if explicit_widget:
            return explicit_widget

        if field.choices:
            if field.is_multiple:
                return "multiselect"

            return "select"

        return super().get_widget(
            field
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
        request=None,
        instance=None,
    ):
        schema = super().get_schema(
            field,
            request=request,
            instance=instance,
        )

        if field.choices:
            schema["options"] = field.choices

        autocomplete = self.get_option(
            field,
            "autocomplete",
        )

        if autocomplete:
            schema["autocomplete"] = autocomplete

        min_length = self.get_min_length(
            field
        )

        if min_length:
            schema["minLength"] = min_length

        max_length = self.get_max_length(
            field
        )

        if max_length:
            schema["maxLength"] = max_length

        return schema