# =========================================================
# accessor.py
# =========================================================

class BaseValueAccessor:
    """
    Абстракция хранения значения.

    Поле НЕ знает где лежит value:
    - django field
    - dynamic table
    - json
    - api
    - cache
    - computed
    """

    def get(
        self,
        obj,
        field,
    ):
        raise NotImplementedError

    def set(
        self,
        obj,
        field,
        value,
    ):
        raise NotImplementedError