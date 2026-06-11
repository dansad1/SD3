# =========================================================
# backend/dynamic/field_types/richtext.py
# =========================================================

import bleach

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)


@register_field_type
class RichTextFieldType(StringFieldType):

    code = "richtext"

    label = "RichText"

    widget = "richtext"

    searchable = True

    sortable = False

    filterable = False

    DEFAULT_MAX_LENGTH = 100000

    ABSOLUTE_MAX_LENGTH = 500000

    ALLOWED_TAGS = [
        "p",
        "br",
        "strong",
        "b",
        "em",
        "i",
        "u",
        "s",
        "ul",
        "ol",
        "li",
        "blockquote",
        "pre",
        "code",
        "a",
    ]

    ALLOWED_ATTRIBUTES = {
        "a": [
            "href",
            "title",
            "target",
            "rel",
        ],
    }

    ALLOWED_PROTOCOLS = [
        "http",
        "https",
        "mailto",
    ]

    DANGEROUS_TEXT = (
        "<script",
        "</script",
        "javascript:",
        "data:",
        "vbscript:",
        "onerror",
        "onload",
        "onclick",
        "onmouseover",
        "onfocus",
        "onblur",
    )

    # =====================================================
    # SANITIZE
    # =====================================================

    def sanitize(
        self,
        value,
    ):

        if value is None:
            return None

        raw = str(
            value
        )

        lowered = raw.lower()

        for marker in self.DANGEROUS_TEXT:

            if marker in lowered:

                raise ValidationError(
                    "HTML содержит недопустимый код"
                )

        cleaned = bleach.clean(
            raw,
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            protocols=self.ALLOWED_PROTOCOLS,
            strip=True,
            strip_comments=True,
        )

        cleaned = bleach.linkify(
            cleaned,
            callbacks=[
                bleach.callbacks.nofollow,
            ],
            skip_tags=[
                "pre",
                "code",
            ],
        )

        return cleaned

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

        if field.is_multiple:

            return [
                self.sanitize(v)
                for v in value
            ]

        return self.sanitize(
            value
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

        if field.is_multiple:

            return [
                self.sanitize(v)
                for v in value
            ]

        return self.sanitize(
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

        return self.normalize(
            field,
            value,
        )

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

            "html":
                True,

            "sanitize":
                True,

            "allowedTags":
                self.ALLOWED_TAGS,

            "maxLength":
                field.max_value
                or self.DEFAULT_MAX_LENGTH,
        })

        return schema