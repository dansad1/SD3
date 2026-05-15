from backend.engine.entity.EntityRegistry import (
    entity_registry
)


def collect_permissions():

    permissions = set()

    for entity in (
        entity_registry
        .storage
        .by_code
        .values()
    ):

        capabilities = getattr(
            entity,
            "capabilities",
            {},
        ) or {}

        permissions.update(
            capabilities.values()
        )

    return sorted(permissions)