# backend/engine/permissions/collect_permissions.py

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


SCOPE_LEVELS = (
    "own",
    "company",
    "region",
    "all",
)


def collect_permissions():
    """
    Собирает permission-коды зарегистрированных сущностей.

    Для сущностей с scoped_permissions=True дополнительно создаёт
    варианты own, company, region и all.
    """

    permissions = set()

    entities = (
        entity_registry
        .storage
        .by_code
        .values()
    )

    for entity in entities:
        capabilities = getattr(
            entity,
            "capabilities",
            {},
        ) or {}

        scoped = bool(
            getattr(
                entity,
                "scoped_permissions",
                False,
            )
        )

        for permission in capabilities.values():
            if not permission:
                continue

            permissions.add(
                permission,
            )

            if not scoped:
                continue

            for level in SCOPE_LEVELS:
                permissions.add(
                    f"{permission}_{level}",
                )

    return sorted(
        permissions,
    )