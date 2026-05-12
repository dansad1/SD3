import json
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError




def serialize_dynamic_value(value):
    if value is None:
        return None

    if isinstance(value, (list, dict, bool, int, float)):
        return json.dumps(value, ensure_ascii=False)

    return str(value)


def deserialize_dynamic_value(raw):
    if raw in ("", None):
        return None

    try:
        return json.loads(raw)
    except Exception:
        return raw


def save_dynamic_values(entity_code, obj, data):
    if not data:
        return

    content_type = ContentType.objects.get_for_model(obj)

    fields = DynamicField.objects.filter(
        entity=entity_code,
        name__in=data.keys(),
    )

    field_map = {f.name: f for f in fields}

    errors = {}

    for name, value in data.items():
        field = field_map.get(name)

        if not field:
            continue

        if field.required and value in ("", None, []):
            errors[name] = ["Обязательное поле"]
            continue

        if field.is_multiple and not isinstance(value, list):
            errors[name] = ["Ожидался список"]
            continue

        DynamicValue.objects.update_or_create(
            field=field,
            content_type=content_type,
            object_id=obj.pk,
            defaults={
                "value": serialize_dynamic_value(value)
            }
        )

    if errors:
        raise ValidationError(errors)


def load_dynamic_values(entity_code, obj):
    content_type = ContentType.objects.get_for_model(obj)

    values = DynamicValue.objects.filter(
        field__entity=entity_code,
        content_type=content_type,
        object_id=obj.pk,
    ).select_related("field")

    result = {}

    for item in values:
        result[item.field.name] = deserialize_dynamic_value(item.value)

    return result