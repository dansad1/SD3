class EntityImportExportSerializer:

    def __init__(
        self,
        service,
    ):
        self.service = service

    def serialize_object(
        self,
        obj,
        fields,
    ):
        row = {}

        for field in fields:
            value = field.get_value(
                obj,
            )

            value = field.serialize(
                value,
            )

            row[field.name] = (
                self.service.safe_value(
                    value,
                )
            )

        return row

    def deserialize_row(
        self,
        row,
        fields,
    ):
        data = {}
        errors = {}

        field_map = self.service.get_field_map(
            fields,
        )

        for name, raw_value in row.items():
            field = field_map.get(
                name,
            )

            if not field:
                continue

            try:
                value = field.deserialize(
                    raw_value,
                )

                value = field.normalize(
                    value,
                )

                field.validate(
                    value,
                )

                data[name] = value

            except Exception as exc:
                errors[name] = str(
                    exc,
                )

        return data, errors