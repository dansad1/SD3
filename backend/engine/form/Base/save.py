from django.core.exceptions import PermissionDenied


def save(ctx):
    model = ctx.model
    data = ctx.data

    if ctx.mode == "create":
        obj = model(**data)

    elif ctx.mode == "edit":
        obj = ctx.instance

        if not obj:
            raise PermissionDenied

        for key, value in data.items():
            setattr(obj, key, value)

    else:
        raise PermissionDenied

    obj.full_clean()
    obj.save()

    for key, items in ctx.m2m.items():
        getattr(obj, key).set(items)

    ctx.instance = obj
    return obj