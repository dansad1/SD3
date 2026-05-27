from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


# =========================================================
# ACCESSOR
# =========================================================

class PasswordAccessor:

    # =====================================================
    # READ
    # =====================================================

    def get(
        self,
        obj,
        field,
    ):
        """
        Никогда не возвращаем hash.
        """

        return None

    # =====================================================
    # WRITE
    # =====================================================

    def set(
        self,
        obj,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return

        obj.set_password(
            value
        )


# =========================================================
# FIELD TYPE
# =========================================================

@register_field_type
class PasswordFieldType(BaseFieldType):

    code = "password"

    label = "Password"

    # =====================================================
    # SECURITY
    # =====================================================

    serializeable = False

    searchable = False

    filterable = False

    # =====================================================
    # ACCESSOR
    # =====================================================

    accessor = PasswordAccessor()

    # =====================================================
    # UI
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({
            "inputType": "password",
        })

        return schema

    # =====================================================
    # NORMALIZE
    # =====================================================

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

        return str(value)

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        """
        Никогда не сериализуем password/hash.
        """

        return None