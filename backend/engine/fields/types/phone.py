import phonenumbers

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class PhoneFieldType(
    StringFieldType
):

    code = "phone"

    label = "Phone"

    widget = "phone"

    searchable = True
    sortable = True
    filterable = True

    features = [
        "required",
        "unique",
        "placeholder",
        "help_text",
    ]

    DEFAULT_REGION = "RU"

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_phone(
        self,
        value,
    ):

        if not isinstance(
            value,
            (
                str,
                int,
            ),
        ):
            raise ValidationError(
                "Некорректный номер"
            )

        raw = str(
            value
        ).strip()

        if not raw:

            raise ValidationError(
                "Некорректный номер"
            )

        try:

            parsed = phonenumbers.parse(

                raw,

                self.DEFAULT_REGION,

            )

        except Exception:

            raise ValidationError(
                "Некорректный номер"
            )

        if not (

            phonenumbers.is_possible_number(

                parsed

            )

        ):

            raise ValidationError(

                "Некорректный номер"

            )

        if not (

            phonenumbers.is_valid_number(

                parsed

            )

        ):

            raise ValidationError(

                "Некорректный номер"

            )

        return phonenumbers.format_number(

            parsed,

            phonenumbers

            .PhoneNumberFormat

            .E164,

        )

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

                self.to_phone(v)

                for v in value

            ]

        return self.to_phone(

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

        try:

            if field.is_multiple:

                return [

                    self.to_phone(v)

                    for v in value

                ]

            return self.to_phone(

                value

            )

        except ValidationError:

            return value

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def serialize(

        self,

        field,

        value,

    ):

        if value in (

            None,

            "",

        ):

            return None

        try:

            if field.is_multiple:

                return [

                    self.to_phone(v)

                    for v in value

                ]

            return self.to_phone(

                value

            )

        except ValidationError:

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

        if value in (

            None,

            "",

        ):

            return None

        try:

            if field.is_multiple:

                return [

                    self.to_phone(v)

                    for v in value

                ]

            return self.to_phone(

                value

            )

        except ValidationError:

            #
            # Не валим список компаний
            #

            return str(

                value

            )

    # =====================================================
    # FILTER
    # =====================================================

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

        try:

            value = self.to_phone(

                value

            )

        except ValidationError:

            return queryset.none()

        return queryset.filter(

            **{

                field.name:

                    value

            }

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

            "autocomplete":

                "tel",

            "defaultRegion":

                self.DEFAULT_REGION,

        })

        return schema