def get_queryset(ctx):
    entity = ctx.entity

    qs = entity.model.objects.all()

    if entity.soft_delete and hasattr(entity.model, "is_deleted"):
        qs = qs.filter(is_deleted=False)

    return entity.apply_user_scope(ctx.request, qs)