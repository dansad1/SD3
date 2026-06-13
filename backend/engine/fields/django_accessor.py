from backend.engine.fields.value import (
    BaseValueAccessor,
)


class DjangoFieldAccessor(
    BaseValueAccessor
):

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        obj,
        field,
    ):

        value = getattr(
            obj,
            field.name,
            None,
        )

        if field.is_multiple:

            if value is None:
                return []

            return list(
                value.all()
            )

        return value

    # =====================================================
    # SET
    # =====================================================

    def set(
        self,
        obj,
        field,
        value,
    ):

        if field.is_multiple:

            getattr(
                obj,
                field.name,
            ).set(
                value or []
            )

            return value

        setattr(
            obj,
            field.name,
            value,
        )

        return value