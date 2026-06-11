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

    widget = "json"

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

    MAX_TOTAL_SIZE = 1024 * 1024

    DANGEROUS_KEYS = {
        "__proto__",
        "constructor",
        "prototype",
    }

    # =====================================================
    # PARSE
    # =====================================================

    def parse_json(
        self,
        value,
    ):

        if isinstance(
            value,
            str,
        ):

            try:

                return json.loads(
                    value
                )

            except Exception:

                raise ValidationError(
                    "Некорректный JSON"
                )

        return value

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

        value = self.parse_json(
            value
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

        if depth > self.MAX_DEPTH:

            raise ValidationError(
                "JSON слишком вложенный"
            )

        if value is None:
            return

        if isinstance(
            value,
            bool,
        ):
            return

        if isinstance(
            value,
            (
                int,
                float,
            ),
        ):

            if (
                isinstance(
                    value,
                    float,
                )
                and not math.isfinite(
                    value
                )
            ):

                raise ValidationError(
                    "Некорректное число"
                )

            return

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

                if not isinstance(
                    key,
                    str,
                ):

                    raise ValidationError(
                        "Ключ JSON должен быть строкой"
                    )

                if len(key) > 255:

                    raise ValidationError(
                        "Слишком длинный ключ"
                    )

                if (
                    key
                    in self.DANGEROUS_KEYS
                ):

                    raise ValidationError(
                        "Недопустимый ключ JSON"
                    )

                self.validate_json(
                    item,
                    depth + 1,
                )

            return

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

        return self.parse_json(
            value
        )

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

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "json":
                True,

            "maxDepth":
                self.MAX_DEPTH,

            "maxSize":
                self.MAX_TOTAL_SIZE,
        })

        return schema