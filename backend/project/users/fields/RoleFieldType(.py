from backend.engine.fields.types.DomainRelationFieldType import DomainRelationFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class RoleFieldType(
    DomainRelationFieldType,
):
    code = "role"
    label = "Role"
    entity_name = "roles"
