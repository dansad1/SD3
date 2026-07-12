import json
import logging

from django.core.exceptions import ValidationError

from backend.generic.models import DynamicField

logger = logging.getLogger(__name__)


class DynamicValueService:

    @staticmethod
    def decode(
        value,
    ):

        if value in (
            None,
            "",
        ):
            return None

        if not isinstance(
            value,
            str,
        ):
            return value

        try:

            return json.loads(
                value,
            )

        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):

            return value

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

                raw = cls.decode(
                    item.value,
                )

                values[
                    item.field.name
                ] = field.deserialize(
                    raw,
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
            ).get(
                name,
                default,
            )
        )