from .serializer import (
    EntityImportExportSerializer,
)


class EntityExporter:

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

    def get_headers(
        self,
        fields,
    ):
        return [
            {
                "name": field.name,
                "label": self.service.safe_value(
                    field.label,
                ),
            }
            for field in fields
        ]

    def export_queryset(
        self,
        queryset,
    ):
        fields = (
            self.service.get_export_fields()
        )

        print("=" * 80)
        print("EXPORT START")
        print("ENTITY:", self.service.entity.entity)
        print("FIELDS:")
        print([
            field.name
            for field in fields
        ])
        print("=" * 80)

        rows = []

        for obj in queryset:

            print("-" * 80)
            print(
                "OBJECT:",
                obj,
            )

            try:
                row = (
                    self.serializer.serialize_object(
                        obj,
                        fields,
                    )
                )

                print(
                    "ROW:",
                    row,
                )

                rows.append(
                    row,
                )

            except Exception as exc:

                print("=" * 80)
                print(
                    "EXPORT FAILED"
                )
                print(
                    "OBJECT:",
                    obj,
                )
                print(
                    "ERROR:",
                    repr(exc),
                )
                print("=" * 80)

                raise

        print("=" * 80)
        print(
            "EXPORT OK",
            len(rows),
            "rows",
        )
        print("=" * 80)

        return {
            "headers": self.get_headers(
                fields,
            ),
            "rows": rows,
        }

    def export_template(
        self,
    ):
        fields = (
            self.service.get_template_fields()
        )

        print("=" * 80)
        print("EXPORT TEMPLATE")
        print([
            field.name
            for field in fields
        ])
        print("=" * 80)

        return {
            "headers": self.get_headers(
                fields,
            ),
            "rows": [],
        }