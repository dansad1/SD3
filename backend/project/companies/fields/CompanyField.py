from backend.engine.fields.types.DomainRelationFieldType import (
    DomainRelationFieldType,
)
from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class CompanyFieldType(
    DomainRelationFieldType,
):

    code = "company"

    label = "Company"

    entity_name = "company"

    provider = "company"