class RelationProviderRegistry:

    def __init__(self):
        self.providers = {}

    def register(
        self,
        provider_cls,
    ):
        provider = provider_cls()

        if not provider.code:
            raise RuntimeError(
                "Relation provider code is required."
            )

        if provider.code in self.providers:
            raise RuntimeError(
                f"Relation provider '{provider.code}' already registered."
            )

        self.providers[
            provider.code
        ] = provider

    def get(
        self,
        code,
    ):
        provider = self.providers.get(
            code
        )

        if provider is None:
            raise RuntimeError(
                f"Unknown relation provider '{code}'."
            )

        return provider


relation_provider_registry = (
    RelationProviderRegistry()
)


def register_relation_provider(
    cls,
):
    relation_provider_registry.register(
        cls
    )
    return cls