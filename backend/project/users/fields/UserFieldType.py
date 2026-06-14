from backend.engine.fields.types.DomainRelationFieldType import DomainRelationFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class UserFieldType(
    DomainRelationFieldType,
):
    code = "user"
    label = "User"
    entity_name = "user"
