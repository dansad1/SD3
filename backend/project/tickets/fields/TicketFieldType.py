from backend.engine.fields.types.DomainRelationFieldType import DomainRelationFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class TicketTypeFieldType(
    DomainRelationFieldType,
):
    code = "ticket"
    label = "Ticket Type"
    entity_name = "ticket-type"
