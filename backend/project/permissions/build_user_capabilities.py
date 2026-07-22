# backend/engine/permissions/build_user_capabilities.py

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


SCOPE_LEVELS = (
    "all",
    "region",
    "company",
    "own",
)


def get_scope_level(
    request,
    entity,
    action,
):
    user = getattr(
        request,
        "user",
        None,
    )

    if (
        user is None
        or not user.is_authenticated
    ):
        return "none"

    if user.is_superuser:
        return "all"

    capabilities = getattr(
        entity,
        "capabilities",
        {},
    ) or {}

    base_permission = capabilities.get(
        action,
    )

    if not base_permission:
        return "none"

    role = getattr(
        user,
        "role",
        None,
    )

    if role is None:
        return "none"

    for level in SCOPE_LEVELS:
        permission_code = (
            f"{base_permission}_{level}"
        )

        if role.permissions.filter(
            code=permission_code,
        ).exists():
            return level

    return "none"


def build_user_capabilities(
    request,
):
    """
    Возвращает capabilities пользователя для DSL.

    Обычная сущность:

    {
        "roles": {
            "list": True,
            "view": True,
            "create": True,
            "edit": True,
            "delete": True,
        },
    }

    Scoped-сущность:

    {
        "tickets": {
            "list": True,
            "view": True,
            "create": True,
            "edit": True,
            "delete": False,
            "_scopes": {
                "list": "region",
                "view": "region",
                "create": "company",
                "edit": "own",
                "delete": "none",
            },
        },
    }
    """

    result = {}

    entities = (
        entity_registry
        .storage
        .by_code
        .values()
    )

    for entity in entities:
        capabilities = (
            entity.get_capabilities_for_user(
                request,
            )
            or {}
        )

        entity_code = entity.entity

        entity_result = result.setdefault(
            entity_code,
            {},
        )

        scoped = bool(
            getattr(
                entity,
                "scoped_permissions",
                False,
            )
        )

        if scoped:
            scopes_result = entity_result.setdefault(
                "_scopes",
                {},
            )
        else:
            scopes_result = None

        for action, base_allowed in capabilities.items():
            if not scoped:
                entity_result[action] = bool(
                    base_allowed,
                )
                continue

            scope = get_scope_level(
                request=request,
                entity=entity,
                action=action,
            )

            scopes_result[action] = scope

            entity_result[action] = bool(
                base_allowed
                and scope != "none"
            )

    return result