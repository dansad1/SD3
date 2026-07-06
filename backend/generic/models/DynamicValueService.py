from backend.generic.models import DynamicField


class DynamicValueService:

    @classmethod
    def get_map(
        cls,
        instance,
    ):

        values = {}

        queryset = (
            instance.dynamic_values
            .select_related(
                "field",
            )
            .all()
        )

        for item in queryset:

            field = DynamicField(
                item.field,
            )

            values[
                item.field.name
            ] = field.deserialize(
                item.value,
            )

        return values

    @classmethod
    def get(
        cls,
        instance,
        name,
        default=None,
    ):

        if hasattr(
            instance,
            name,
        ):
            return getattr(
                instance,
                name,
            )

        return (
            cls.get_map(
                instance,
            )
            .get(
                name,
                default,
            )
        )