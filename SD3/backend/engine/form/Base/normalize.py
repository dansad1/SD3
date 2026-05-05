from django.db import models
from django.core.exceptions import FieldDoesNotExist, ValidationError


EMPTY_VALUES = ("", None)


def extract_id(value):
    if value in EMPTY_VALUES:
        return None

    if isinstance(value, dict):
        relation_id = value.get("value")

        if relation_id in EMPTY_VALUES:
            relation_id = value.get("id")

        if relation_id in EMPTY_VALUES:
            raise ValidationError("Invalid relation object")

        return relation_id

    return value


def normalize_m2m_value(name, value):
    if value in EMPTY_VALUES:
        return []

    if not isinstance(value, list):
        raise ValidationError({
            name: ["Expected list"]
        })

    ids = []

    for item in value:
        relation_id = extract_id(item)

        if relation_id in EMPTY_VALUES:
            continue

        ids.append(relation_id)

    return ids


def normalize_json_value(value):
    if isinstance(value, list):
        result = []

        for item in value:
            if isinstance(item, dict) and ("value" in item or "id" in item):
                result.append(extract_id(item))
            else:
                result.append(item)

        return result

    return value


def normalize_dynamic_value(form_field, value):
    field_type = form_field.get("type")
    multiple = form_field.get("multiple") or form_field.get("is_multiple")

    if value in EMPTY_VALUES:
        if multiple:
            return []
        return None

    if multiple:
        if not isinstance(value, list):
            raise ValidationError({
                form_field["name"]: ["Expected list"]
            })

        return [
            extract_id(item) if isinstance(item, dict) else item
            for item in value
            if item not in EMPTY_VALUES
        ]

    if isinstance(value, dict) and ("value" in value or "id" in value):
        return extract_id(value)

    if field_type in ("boolean", "bool"):
        if value in ["true", "True", 1, "1", True]:
            return True
        if value in ["false", "False", 0, "0", False]:
            return False
        return bool(value)

    return value


def normalize(ctx):
    clean = {}
    m2m = {}
    dynamic = {}

    allowed_names = {f["name"] for f in ctx.fields}

    for form_field in ctx.fields:
        name = form_field["name"]

        if name not in allowed_names:
            continue

        if form_field.get("readonly"):
            continue

        if name not in ctx.payload:
            continue

        value = ctx.payload.get(name)

        try:
            field = ctx.model._meta.get_field(name)
        except FieldDoesNotExist:
            dynamic[name] = normalize_dynamic_value(form_field, value)
            continue

        if isinstance(field, models.ForeignKey):
            relation_id = extract_id(value)

            if relation_id in EMPTY_VALUES:
                clean[name] = None
            else:
                related_model = field.remote_field.model

                try:
                    clean[name] = related_model.objects.get(pk=relation_id)
                except related_model.DoesNotExist:
                    raise ValidationError({
                        name: ["Related object not found"]
                    })

            continue

        if isinstance(field, models.ManyToManyField):
            ids = normalize_m2m_value(name, value)

            related_model = field.remote_field.model
            objects = list(related_model.objects.filter(pk__in=ids))

            found_ids = {str(obj.pk) for obj in objects}
            requested_ids = {str(i) for i in ids}

            missing = requested_ids - found_ids

            if missing:
                raise ValidationError({
                    name: [f"Related objects not found: {', '.join(missing)}"]
                })

            m2m[name] = objects
            continue

        if isinstance(field, models.JSONField):
            clean[name] = normalize_json_value(value)
            continue

        if isinstance(field, models.BooleanField):
            if value in ["true", "True", 1, "1", True]:
                clean[name] = True
            elif value in ["false", "False", 0, "0", False]:
                clean[name] = False
            else:
                clean[name] = bool(value)
            continue

        clean[name] = value

    ctx.data = clean
    ctx.m2m = m2m
    ctx.dynamic = dynamic

    return ctx