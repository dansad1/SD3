# =========================================================
# django_accessor.py
# =========================================================
from backend.engine.fields.value import BaseValueAccessor


class DjangoFieldAccessor(
    BaseValueAccessor
):

    def get(
        self,
        obj,
        field,
    ):

        return getattr(
            obj,
            field.name,
            None,
        )

    def set(
        self,
        obj,
        field,
        value,
    ):

        setattr(
            obj,
            field.name,
            value,
        )

        return value