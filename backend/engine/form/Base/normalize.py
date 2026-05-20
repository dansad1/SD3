from rest_framework.exceptions import ValidationError

from backend.engine.entity.EntityRegistry import entity_registry


def normalize(
    self,
    field,
    value,
):

    if value in (
        None,
        "",
    ):
        return None

    if isinstance(
        value,
        dict,
    ):

        value = (
            value.get("value")
            or value.get("id")
        )

    entity = entity_registry.get(
        field.relation_entity
    )

    model = entity.model

    if field.is_multiple:

        if not isinstance(
            value,
            list,
        ):
            raise ValidationError(
                "Expected list"
            )

        return list(
            model.objects.filter(
                pk__in=value
            )
        )

    return model.objects.get(
        pk=value
    )