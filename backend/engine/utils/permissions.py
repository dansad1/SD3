def has_permission(ctx, action) -> bool:
    entity = ctx.entity
    user = ctx.request.user

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    code = (entity.capabilities or {}).get(action)

    if not code:
        return True

    role = getattr(user, "role", None)

    return (
        role.permissions.filter(code=code).exists()
        if role else False
    )