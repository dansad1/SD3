from django.core.exceptions import ValidationError

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class BooleanFieldType(BaseFieldType):

    code = "boolean"

    label = "Boolean"

    widget = "checkbox"

    sortable = True
    searchable = False
    filterable = True

    features = [
        "default_value",
        "help_text",
        "required",
    ]

    default_value_widget = "checkbox"

    TRUE_VALUES = {
        True,
        1,
        "1",
        "true",
        "True",
        "TRUE",
        "yes",
        "Yes",
        "YES",
        "on",
        "ON",
    }

    FALSE_VALUES = {
        False,
        0,
        "0",
        "false",
        "False",
        "FALSE",
        "no",
        "No",
        "NO",
        "off",
        "OFF",
    }

    def to_bool(
        self,
        value,
    ):

        if value in self.TRUE_VALUES:
            return True

        if value in self.FALSE_VALUES:
            return False

        raise ValidationError(
            "Некорректное булево значение"
        )

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
                self.to_bool(v)
                for v in value
            ]

        return self.to_bool(
            value
        )

    def normalize(
        self,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return None

        if field.is_multiple:
            return [
                self.to_bool(v)
                for v in value
            ]

        return self.to_bool(
            value
        )

    def serialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        return bool(value)

    def deserialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        return self.to_bool(
            value
        )

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return queryset

        return queryset.filter(
            **{
                field.name:
                    self.to_bool(value)
            }
        )

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "inputType":
                "checkbox",

            "builder": {

                "features":
                    self.features,

                "defaultValueWidget":
                    self.default_value_widget,

            }

        })

        return schema