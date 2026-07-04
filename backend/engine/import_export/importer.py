from django.core.exceptions import ValidationError
from django.db import transaction

from .serializer import (
    EntityImportExportSerializer,
)


class EntityImporter:

    def __init__(
        self,
        service,
    ):
        self.service = service

        self.serializer = (
            EntityImportExportSerializer(
                service,
            )
        )

    def preview(
        self,
        headers,
        rows,
    ):
        fields = (
            self.service.get_import_fields()
        )

        result = []
        errors = {}

        for row_number, row in enumerate(
            rows,
            start=3,
        ):

            source = {}

            for index, header in enumerate(
                headers,
            ):
                if not header:
                    continue

                source[header] = (
                    row[index]
                    if index < len(row)
                    else None
                )

            data, row_errors = (
                self.serializer.deserialize_row(
                    source,
                    fields,
                )
            )

            if row_errors:
                errors[row_number] = (
                    row_errors
                )

            result.append(
                {
                    "row": row_number,
                    "data": data,
                }
            )

        return {
            "rows": result,
            "errors": errors,
        }

    @transaction.atomic
    def commit(
        self,
        rows,
    ):
        created = 0
        updated = 0

        field_map = (
            self.service.get_field_map(
                self.service.get_import_fields(),
            )
        )

        for row in rows:

            data = row.get(
                "data",
                {},
            )

            lookup = data.get(
                self.service.lookup_field,
            )

            if not lookup:
                raise ValidationError({
                    self.service.lookup_field: (
                        "Нет ключевого поля"
                    )
                })

            instance, is_created = (
                self.service.entity.model.objects.get_or_create(
                    **{
                        self.service.lookup_field: lookup,
                    }
                )
            )

            for name, value in data.items():

                field = field_map.get(
                    name,
                )

                if field is None:
                    continue

                field.set_value(
                    instance,
                    value,
                )

            instance.full_clean()
            instance.save()

            if is_created:
                created += 1
            else:
                updated += 1

        return {
            "created": created,
            "updated": updated,
            "total": len(rows),
        }