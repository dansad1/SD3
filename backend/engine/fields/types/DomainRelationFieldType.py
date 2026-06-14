from backend.engine.fields.types.relation import (
    RelationFieldType,
)

from backend.engine.fields.providers.registry import (
    relation_provider_registry,
)


class DomainRelationFieldType(
    RelationFieldType,
):

    code = None

    label = None

    entity_name = None

    def get_entity_name(
        self,
        field,
    ):
        return self.entity_name

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):

        provider = (
            field.options.get(
                "provider"
            )
        )

        if provider:

            return (
                relation_provider_registry.execute(
                    provider=provider,
                    field=field,
                    request=request,
                    instance=instance,
                )
            )

        return super().get_options(
            field,
            request,
            instance,
        )