# backend/engine/fields/types/email.py

import re

from django.core.validators import (
    validate_email,
)

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)


# =====================================================
# CONSTANTS
# =====================================================

MAX_EMAIL_LENGTH = 254

LOCAL_MAX_LENGTH = 64

DOMAIN_MAX_LENGTH = 253

# =====================================================
# REGEX
# =====================================================

EMAIL_RE = re.compile(

    r"^[^\s@]+@[^\s@]+\.[^\s@]+$",

    re.IGNORECASE,
)

# =====================================================
# FIELD TYPE
# =====================================================

# backend/engine/fields/types/email.py

from backend.engine.fields.types.string import (
    StringFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class EmailFieldType(
    StringFieldType
):

    code = "email"

    label = "Email"