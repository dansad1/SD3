from django.db import models
from django.core.exceptions import FieldDoesNotExist

from SD3.backend.engine.form.Base.services import load_dynamic_values


def serialize_fk(value):
    if not value:
        return None

    return {
        "value": value.pk,
        "label": str(value),
    }


def serialize(ctx):
    if not ctx.instance:
        ctx.data = {}
        return ctx

    data = {"id": ctx.instance.pk}

    for f in ctx.fields:
        name = f["name"]

        try:
            field = ctx.model._meta.get_field(name)
        except FieldDoesNotExist:
            continue

        value = getattr(ctx.instance, name)

        if isinstance(field, models.ForeignKey):
            data[name] = serialize_fk(value)
            continue

        if isinstance(field, models.ManyToManyField):
            data[name] = [
                serialize_fk(obj) for obj in value.all()
            ]
            continue

        data[name] = value

    dynamic_data = load_dynamic_values(
        entity_code=ctx.entity.entity,
        obj=ctx.instance,
    )

    data.update(dynamic_data)

    ctx.data = data
    return ctx