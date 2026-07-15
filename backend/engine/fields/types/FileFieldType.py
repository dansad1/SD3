from django.core.exceptions import ValidationError

from backend.engine.fields.types.base import (
    BaseFieldType,
)
from backend.engine.fields.types.registry import (
    register_field_type,
)
from backend.generic.models import (
    StoredFile,
)


@register_field_type
class FileFieldType(BaseFieldType):
    code = "file"
    label = "Файл"
    widget = "file"

    sortable = False
    searchable = False
    filterable = False

    features = [
        "required",
        "help_text",
        "accept",
        "max_size",
        "max_files",
    ]

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
            self,
            field,
            value,
    ):

        value = super().validate(
            field,
            value,
        )

        if value in (
                None,
                "",
                [],
        ):
            return [] if field.is_multiple else None

        if field.is_multiple:

            if not isinstance(
                    value,
                    (
                            list,
                            tuple,
                    ),
            ):
                value = [value]

            return [
                self.validate_file(item)
                for item in value
            ]

        return self.validate_file(value)

    # =====================================================
    # FILE
    # =====================================================

    def validate_file(
            self,
            value,
    ):

        if isinstance(
                value,
                dict,
        ):
            value = (
                    value.get("id")
                    or value.get("value")
            )

        try:
            value = int(value)

        except (
                TypeError,
                ValueError,
        ):
            raise ValidationError(
                "Некорректный файл",
            )

        if not StoredFile.objects.filter(
                pk=value,
        ).exists():
            raise ValidationError(
                "Файл не найден",
            )

        return value

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
            self,
            field,
            value,
    ):
        return value

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
            self,
            field,
            value,
    ):

        if value in (
                None,
                "",
                [],
        ):
            return [] if field.is_multiple else None

        if field.is_multiple:

            if not isinstance(
                    value,
                    (
                            list,
                            tuple,
                    ),
            ):
                value = [value]

            result = []

            for item in value:

                if isinstance(
                        item,
                        dict,
                ):
                    item = (
                            item.get("id")
                            or item.get("value")
                    )

                result.append(
                    int(item)
                )

            return result

        if isinstance(
                value,
                dict,
        ):
            value = (
                    value.get("id")
                    or value.get("value")
            )

        return int(value)

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
            self,
            field,
            value,
    ):

        if value in (
                None,
                "",
                [],
        ):
            return [] if field.is_multiple else None

        if field.is_multiple:

            if not isinstance(
                    value,
                    (
                            list,
                            tuple,
                    ),
            ):
                value = [value]

            ids = []

            for item in value:
                try:
                    ids.append(
                        int(item)
                    )
                except (
                        TypeError,
                        ValueError,
                ):
                    continue

            files = StoredFile.objects.in_bulk(
                ids,
            )

            return [
                self.serialize_object(
                    files[file_id],
                )
                for file_id in ids
                if file_id in files
            ]

        try:

            file = StoredFile.objects.get(
                pk=int(value),
            )

        except (
                StoredFile.DoesNotExist,
                TypeError,
                ValueError,
        ):

            return None

        return self.serialize_object(
            file,
        )

    # =====================================================
    # DTO
    # =====================================================

    def serialize_object(
            self,
            file,
    ):

        return {
            "id": file.pk,
            "name": file.original_name,
            "size": file.size,
            "mime_type": file.mime_type,
            "url": file.file.url,
        }
