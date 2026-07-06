import logging

from django.core.exceptions import ValidationError

from backend.generic.models import DynamicField
logger = logging.getLogger(__name__)


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

            try:

                values[
                    item.field.name
                ] = field.deserialize(
                    item.value,
                )

            except ValidationError as exc:

                logger.warning(
                    (
                        "Invalid dynamic value. "
                        "Model=%s "
                        "Object=%s "
                        "Field=%s "
                        "Value=%r "
                        "Error=%s"
                    ),
                    instance.__class__.__name__,
                    instance.pk,
                    item.field.name,
                    item.value,
                    exc,
                )

                values[
                    item.field.name
                ] = None

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