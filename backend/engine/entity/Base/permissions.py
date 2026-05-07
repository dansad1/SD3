from rest_framework.exceptions import (
    PermissionDenied
)


# =========================
# GET PERMISSION CODE
# =========================

def get_permission_code(
    entity,
    action,
):

    return (
        entity.capabilities
        or {}
    ).get(action)


# =========================
# CHECK ROLE
# =========================

def has_role_permission(
    role,
    code,
):

    if not role:
        return False

    return role.permissions.filter(
        code=code
    ).exists()


# =========================
# MAIN
# =========================

def has_permission(
    ctx,
    action,
):

    user = ctx.user

    if not user.is_authenticated:
        return False

    code = get_permission_code(
        ctx.entity,
        action,
    )

    # no permission required
    if not code:
        return True

    return has_role_permission(
        getattr(user, "role", None),
        code,
    )


# =========================
# RAISE
# =========================

def check_permission(
    ctx,
    action,
):

    if not has_permission(
        ctx,
        action,
    ):
        raise PermissionDenied


# =========================
# CAPABILITIES
# =========================

def get_capabilities(ctx):

    return {
        action: has_permission(
            ctx,
            action,
        )
        for action in [
            "list",
            "view",
            "create",
            "edit",
            "delete",
        ]
    }