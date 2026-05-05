from django.db import models


def should_include(field, entity):
    """
    Фильтр ТОЛЬКО для Django полей.
    Dynamic поля сюда не попадают.
    """

    # -------------------------
    # TYPE CHECK (ЖЁСТКАЯ ГРАНИЦА)
    # -------------------------
    if not isinstance(field, models.Field):
        return False

    name = field.name

    # -------------------------
    # SYSTEM FILTER
    # -------------------------

    # reverse relations (user_set и т.п.)
    if field.auto_created and not field.concrete:
        return False

    # primary key (обычно не нужен в формах)
    if field.primary_key:
        return False

    # soft delete поля
    if name in {"is_deleted", "deleted_at"}:
        return False

    # не редактируемые
    if not getattr(field, "editable", True):
        return False

    # -------------------------
    # ENTITY CONFIG
    # -------------------------

    include = set(entity.include_fields or [])
    exclude = set(entity.exclude_fields or [])

    # явное исключение
    if name in exclude:
        return False

    # если есть include — только whitelist
    if include:
        return name in include

    return True
def should_include_dynamic(field, entity, request):
    """
    Фильтр для dynamic полей (UserField)
    """

    name = field.name

    include = set(entity.include_fields or [])
    exclude = set(entity.exclude_fields or [])

    if name in exclude:
        return False

    if include:
        return name in include

    # доступы (если есть)
    if hasattr(entity, "can_view_dynamic_field"):
        return entity.can_view_dynamic_field(request, field)

    return True