from django.core.exceptions import PermissionDenied

# permissions.py

def has_permission(ctx, action) -> bool:
    entity = ctx.entity
    user = ctx.user

    if not user.is_authenticated:
        return False

    code = (entity.capabilities or {}).get(action)

    if not code:
        return True

    role = getattr(user, "role", None)

    return (
        role.permissions.filter(code=code).exists()
        if role else False
    )
def check_permission(ctx, action):
    entity = ctx.entity
    code = getattr(entity.capabilities, action, None)

    if not code:
        return

    user = ctx.user

    if not user.is_authenticated:
        raise PermissionDenied

    role = getattr(user, "role", None)
    if not role:
        raise PermissionDenied

    if not role.permissions.filter(code=code).exists():
        raise PermissionDenied


def get_capabilities(ctx):
    entity = ctx.entity
    user = ctx.user

    result = {}

    for action in ["list", "view", "create", "edit", "delete"]:
        code = getattr(entity.capabilities, action, None)

        if not code:
            result[action] = True
            continue

        if not user.is_authenticated:
            result[action] = False
            continue

        role = getattr(user, "role", None)

        result[action] = (
            role.permissions.filter(code=code).exists()
            if role else False
        )

    return result