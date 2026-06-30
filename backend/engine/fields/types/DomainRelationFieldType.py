from backend.engine.fields.providers.registry import (
    relation_provider_registry,
)

from backend.engine.fields.types.relation import (
    RelationFieldType,
)


class DomainRelationFieldType(
    RelationFieldType,
):

    code = None

    label = None

    entity_name = None

    provider = None

    # =====================================================
    # ENTITY
    # =====================================================

    def get_entity_name(
        self,
        field,
    ):
        return self.entity_name

    # =====================================================
    # PROVIDER
    # =====================================================

    def get_provider(
        self,
        field,
    ):
        provider = (
            self.provider
            or field.options.get(
                "provider"
            )
        )

        if not provider:
            return None

        return (
            relation_provider_registry.get(
                provider
            )
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):

        provider = self.get_provider(
            field
        )

        if provider:

            options = provider.get_options(
                field=field,
                request=request,
                instance=instance,
            )

            if options is not None:
                return options

        return super().get_options(
            field,
            request=request,
            instance=instance,
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        value = super().validate(
            field,
            value,
        )

        provider = self.get_provider(
            field,
        )

        if provider:

            value = provider.validate(
                field=field,
                value=value,
            )

        return value

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):

        value = super().normalize(
            field,
            value,
        )

        provider = self.get_provider(
            field,
        )

        if provider:

            value = provider.normalize(
                field=field,
                value=value,
            )

        return value

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):

        provider = self.get_provider(
            field,
        )

        if provider:

            result = provider.serialize(
                field=field,
                value=value,
            )

            if result is not None:
                return result

        return super().serialize(
            field,
            value,
        )

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        provider = self.get_provider(
            field,
        )

        if provider:

            return provider.apply_filter(
                queryset=queryset,
                field=field,
                value=value,
            )

        return super().apply_filter(
            queryset,
            field,
            value,
        )

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        instance,
        field,
        value,
    ):

        provider = self.get_provider(
            field,
        )

        if not provider:

            field.accessor.set(
                instance,
                field,
                value,
            )

            return

        provider.before_save(
            instance=instance,
            field=field,
            value=value,
        )

        provider.save(
            instance=instance,
            field=field,
            value=value,
        )

        provider.after_save(
            instance=instance,
            field=field,
            value=value,
        )