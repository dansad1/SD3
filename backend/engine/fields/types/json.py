# =========================================================
# backend/dynamic/field_types/json_type.py
# =========================================================

import json
import math

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
class JSONFieldType(BaseFieldType):

    code = "json"

    label = "JSON"

    searchable = False

    sortable = False

    filterable = False

    # =====================================================
    # LIMITS
    # =====================================================

    MAX_DEPTH = 10

    MAX_STRING_LENGTH = 10000

    MAX_LIST_ITEMS = 1000

    MAX_OBJECT_KEYS = 1000

    MAX_TOTAL_SIZE = 1024 * 1024  # 1MB

    # =====================================================
    # VALIDATE
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

        # =============================================
        # STRING JSON
        # =============================================

        if isinstance(
            value,
            str,
        ):

            try:

                value = json.loads(
                    value
                )

            except Exception:

                raise ValidationError(
                    "Некорректный JSON"
                )

        # =============================================
        # RECURSIVE VALIDATION
        # =============================================

        self.validate_json(
            value=value,
            depth=0,
        )

        # =============================================
        # SERIALIZABLE
        # =============================================

        try:

            encoded = json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False,
            )

        except Exception:

            raise ValidationError(
                "Некорректный JSON"
            )

        # =============================================
        # SIZE
        # =============================================

        if (
            len(
                encoded.encode(
                    "utf-8"
                )
            )
            > self.MAX_TOTAL_SIZE
        ):

            raise ValidationError(
                "JSON слишком большой"
            )

        return value

    # =====================================================
    # VALIDATE JSON
    # =====================================================

    def validate_json(
        self,
        value,
        depth,
    ):

        # =============================================
        # DEPTH
        # =============================================

        if depth > self.MAX_DEPTH:

            raise ValidationError(
                "JSON слишком вложенный"
            )

        # =============================================
        # NULL
        # =============================================

        if value is None:

            return

        # =============================================
        # BOOL
        # =============================================

        if isinstance(
            value,
            bool,
        ):

            return

        # =============================================
        # NUMBER
        # =============================================

        if isinstance(
            value,
            (
                int,
                float,
            ),
        ):

            if isinstance(
                value,
                float,
            ):

                if not math.isfinite(
                    value
                ):

                    raise ValidationError(
                        "Некорректное число"
                    )

            return

        # =============================================
        # STRING
        # =============================================

        if isinstance(
            value,
            str,
        ):

            if (
                len(value)
                > self.MAX_STRING_LENGTH
            ):

                raise ValidationError(
                    "Слишком длинная строка"
                )

            return

        # =============================================
        # LIST
        # =============================================

        if isinstance(
            value,
            list,
        ):

            if (
                len(value)
                > self.MAX_LIST_ITEMS
            ):

                raise ValidationError(
                    "Слишком большой список"
                )

            for item in value:

                self.validate_json(
                    item,
                    depth + 1,
                )

            return

        # =============================================
        # OBJECT
        # =============================================

        if isinstance(
            value,
            dict,
        ):

            if (
                len(value)
                > self.MAX_OBJECT_KEYS
            ):

                raise ValidationError(
                    "Слишком большой объект"
                )

            for key, item in value.items():

                # =====================================
                # KEY TYPE
                # =====================================

                if not isinstance(
                    key,
                    str,
                ):

                    raise ValidationError(
                        "Ключ JSON должен быть строкой"
                    )

                # =====================================
                # KEY SIZE
                # =====================================

                if len(key) > 255:

                    raise ValidationError(
                        "Слишком длинный ключ"
                    )

                # =====================================
                # PROTOTYPE POLLUTION
                # =====================================

                dangerous = {

                    "__proto__",
                    "constructor",
                    "prototype",
                }

                if key in dangerous:

                    raise ValidationError(
                        "Недопустимый ключ JSON"
                    )

                self.validate_json(
                    item,
                    depth + 1,
                )

            return

        # =============================================
        # INVALID TYPE
        # =============================================

        raise ValidationError(
            "Недопустимый тип JSON"
        )

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

        if isinstance(
            value,
            str,
        ):

            try:

                value = json.loads(
                    value
                )

            except Exception:

                raise ValidationError(
                    "Некорректный JSON"
                )

        return value

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):

        return value

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        return value

    # =====================================================
    # UI
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "json"
        )

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "json": True,

            "maxDepth":
                self.MAX_DEPTH,

            "maxSize":
                self.MAX_TOTAL_SIZE,
        })

        return schema