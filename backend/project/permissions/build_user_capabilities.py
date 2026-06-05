# backend/engine/permissions/build_user_capabilities.py


from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


def build_user_capabilities(request):

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
        )

        for action, allowed in (
            capabilities.items()
        ):

            result[
                f"{entity.entity}.{action}"
            ] = allowed

    return result

