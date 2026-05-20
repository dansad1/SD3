from backend.engine.fields.types.registry import register_field_type
from backend.engine.fields.types.string import StringFieldType


@register_field_type
class TextFieldType(StringFieldType):

    code = "text"

    label = "Text"

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "textarea"
        )