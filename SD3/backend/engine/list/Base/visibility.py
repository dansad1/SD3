from SD3.backend.engine.list.ListApi import UserListSettings


def apply_visibility(ctx):
    entity_name = ctx.entity.entity

    default = (
        ctx.entity.list_display
        or [f["key"] for f in ctx.fields]
    )

    settings = UserListSettings.objects.filter(
        user=ctx.request.user,
        entity=entity_name,
    ).first()

    visible = settings.visible_fields if settings else default
    visible_set = set(visible)

    ctx.fields = [
        f for f in ctx.fields
        if f["key"] in visible_set
    ]