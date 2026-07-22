# backend/engine/permissions/sync_permissions.py

from django.db import (
    transaction,
)

from backend.project.permissions.collect import collect_permissions
from backend.project.users.models import (
    Permission,
)


@transaction.atomic
def sync_permissions():
    """
    Создаёт отсутствующие permissions из registry.

    Существующие permissions не удаляются, чтобы случайно не
    разрушить связи с ролями.
    """

    collected_codes = set(
        collect_permissions()
    )

    if not collected_codes:
        return {
            "total": 0,
            "created": 0,
            "existing": 0,
        }

    existing_codes = set(
        Permission.objects
        .filter(
            code__in=collected_codes,
        )
        .values_list(
            "code",
            flat=True,
        )
    )

    missing_codes = sorted(
        collected_codes - existing_codes
    )

    Permission.objects.bulk_create(
        [
            Permission(
                code=code,
            )
            for code in missing_codes
        ],
        ignore_conflicts=True,
    )

    return {
        "total": len(collected_codes),
        "created": len(missing_codes),
        "existing": len(existing_codes),
    }