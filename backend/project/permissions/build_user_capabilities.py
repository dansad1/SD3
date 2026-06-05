

# backend/engine/permissions/build_user_capabilities.py

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


def build_user_capabilities(request):
    """
    Возвращает дерево capabilities для DSL.

    Было:

    {
        "role.create": True,
        "role.edit": True,
        "user.create": True,
    }

    Стало:

    {
        "role": {
            "create": True,
            "edit": True,
            "view": True,
            "list": True,
        },

        "user": {
            "create": True,
            "edit": False,
        },
    }
    """

    result = {}

    for entity in (
        entity_registry
        .storage
        .by_code
        .values()
    ):

        capabilities = (
            entity.get_capabilities_for_user(
                request
            )
            or {}
        )

        entity_code = entity.entity

        if entity_code not in result:
            result[entity_code] = {}

        for action, allowed in (
            capabilities.items()
        ):
            result[entity_code][action] = bool(
                allowed
            )

    return result

