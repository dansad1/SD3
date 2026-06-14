class RelationProviderRegistry:

    def __init__(self):
        self.providers = {}

    def register(
        self,
        code,
        provider,
    ):
        self.providers[
            code
        ] = provider

    def execute(
        self,
        provider,
        **kwargs,
    ):

        handler = (
            self.providers.get(
                provider
            )
        )

        if not handler:
            raise RuntimeError(
                f"Unknown relation provider: {provider}"
            )

        return handler(
            **kwargs
        )


relation_provider_registry = (
    RelationProviderRegistry()
)