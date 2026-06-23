from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


def test_permissions():

    for entity in (

        entity_registry

        .storage

        .by_code

        .values()

    ):

        for capability in (

            entity.capabilities

            .values()

        ):

            assert capability