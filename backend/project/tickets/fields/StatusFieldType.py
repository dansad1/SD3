from backend.engine.fields.types.DomainRelationFieldType import (
    DomainRelationFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class StatusFieldType(
    DomainRelationFieldType,
):
    code = "status"

    label = "Status"

    entity_name = "ticket_statuses"
