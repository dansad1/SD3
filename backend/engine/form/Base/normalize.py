from django.db import models
from django.core.exceptions import FieldDoesNotExist, ValidationError


EMPTY_VALUES = ("", None)


# =========================
# HELPERS
# =========================

def normalize_bool(value):
    if value in ["true", "True", "1", 1, True]:
        return True

    if value in ["false", "False", "0", 0, False]:
        return False

    return bool(value)


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
            if isinstance(item, dict) and (
                "value" in item or "id" in item
            ):
                result.append(extract_id(item))
            else:
                result.append(item)

        return result

    return value


def normalize_dynamic_value(form_field, value):
    name = form_field["name"]
    field_type = form_field.get("type")
    multiple = (
        form_field.get("multiple")
        or form_field.get("is_multiple")
    )

    if value in EMPTY_VALUES:
        return [] if multiple else None

    if multiple:
        if not isinstance(value, list):
            raise ValidationError({
                name: ["Expected list"]
            })

        return [
            extract_id(item) if isinstance(item, dict) else item
            for item in value
            if item not in EMPTY_VALUES
        ]

    if isinstance(value, dict) and (
        "value" in value or "id" in value
    ):
        return extract_id(value)

    if field_type in ("boolean", "bool"):
        return normalize_bool(value)

    return value


def validate_dynamic_value(form_field, value):
    """
    Место под будущую field-level validation:
    - max_length
    - regex
    - min/max
    - allowed choices
    - custom validators
    """
    return value


# =========================
# MAIN NORMALIZE
# =========================

def normalize(ctx):
    clean = {}
    m2m = {}
    dynamic = {}

    for form_field in ctx.fields:
        name = form_field["name"]

        # readonly не принимаем с фронта
        if form_field.get("readonly"):
            continue

        # PATCH-поведение: нет в payload — не трогаем
        if name not in ctx.payload:
            continue

        value = ctx.payload.get(name)

        try:
            field = ctx.model._meta.get_field(name)

        except FieldDoesNotExist:
            value = normalize_dynamic_value(
                form_field,
                value,
            )

            value = validate_dynamic_value(
                form_field,
                value,
            )

            dynamic[name] = value
            continue

        # =========================
        # FK
        # =========================

        if isinstance(field, models.ForeignKey):
            relation_id = extract_id(value)

            if relation_id in EMPTY_VALUES:
                clean[name] = None
            else:
                related_model = field.remote_field.model

                try:
                    clean[name] = related_model.objects.get(
                        pk=relation_id
                    )
                except related_model.DoesNotExist:
                    raise ValidationError({
                        name: ["Related object not found"]
                    })

            continue

        # =========================
        # M2M
        # =========================

        if isinstance(field, models.ManyToManyField):
            ids = normalize_m2m_value(name, value)

            related_model = field.remote_field.model
            objects = list(
                related_model.objects.filter(pk__in=ids)
            )

            found_ids = {
                str(obj.pk)
                for obj in objects
            }

            requested_ids = {
                str(i)
                for i in ids
            }

            missing = requested_ids - found_ids

            if missing:
                raise ValidationError({
                    name: [
                        "Related objects not found: "
                        + ", ".join(missing)
                    ]
                })

            m2m[name] = objects
            continue

        # =========================
        # JSON
        # =========================

        if isinstance(field, models.JSONField):
            clean[name] = normalize_json_value(value)
            continue

        # =========================
        # BOOLEAN
        # =========================

        if isinstance(field, models.BooleanField):
            clean[name] = normalize_bool(value)
            continue

        # =========================
        # DEFAULT
        # =========================

        clean[name] = value

    ctx.data = clean
    ctx.m2m = m2m
    ctx.dynamic = dynamic

    return ctx