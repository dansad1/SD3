# =========================================================
# django_accessor.py
# =========================================================

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

        # ================================================
        # MANY TO MANY
        # ================================================

        if field.is_multiple:

            if not value:
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

        # ================================================
        # MANY TO MANY
        # ================================================

        if field.is_multiple:

            relation = getattr(
                obj,
                field.name,
            )

            relation.set(
                value or []
            )

            return value

        # ================================================
        # DEFAULT
        # ================================================

        setattr(
            obj,
            field.name,
            value,
        )

        return value