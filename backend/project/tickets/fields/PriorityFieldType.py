from backend.engine.fields.types.DomainRelationFieldType import DomainRelationFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class PriorityFieldType(
    DomainRelationFieldType,
):
    code = "priority"
    label = "Priority"
    entity_name = "ticket_priorities"