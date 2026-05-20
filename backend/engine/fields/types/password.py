from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class PasswordFieldType(BaseFieldType):

    code = "password"
    label = "Password"

    def get_schema(self, field):
        schema = super().get_schema(field)

        schema.update({
            "inputType": "password",
        })

        return schema