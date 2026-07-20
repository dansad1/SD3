from typing import Any

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

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
            return (
                []
                if field.is_multiple
                else None
            )

        if field.is_multiple:
            values = self.ensure_list(
                value,
            )

            return [
                self.validate_file(item)
                for item in values
            ]

        return self.validate_file(
            value,
        )

    def validate_file(
        self,
        value,
    ):
        file_id = self.extract_id(
            value,
        )

        if file_id is None:
            raise ValidationError(
                "Некорректный файл",
            )

        if not StoredFile.objects.filter(
            pk=file_id,
        ).exists():
            raise ValidationError(
                "Файл не найден",
            )

        return file_id

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):
        if value in (
            None,
            "",
            [],
        ):
            return (
                []
                if field.is_multiple
                else None
            )

        if field.is_multiple:
            result = []

            for item in self.ensure_list(
                value,
            ):
                file_id = self.extract_id(
                    item,
                )

                if file_id is None:
                    continue

                if file_id not in result:
                    result.append(
                        file_id,
                    )

            return result

        return self.extract_id(
            value,
        )

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        """
        Сериализация из модели в initial формы.

        Frontend должен получить не [5, 6, 7], а:

        [
            {
                "id": 5,
                "name": "document.docx",
                "size": 123,
                "mime_type": "...",
                "url": "...",
            },
        ]
        """

        if value in (
            None,
            "",
            [],
        ):
            return (
                []
                if field.is_multiple
                else None
            )

        if field.is_multiple:
            return self.serialize_multiple(
                value,
            )

        return self.serialize_single(
            value,
        )

    def serialize_multiple(
        self,
        value,
    ):
        values = self.ensure_list(
            value,
        )

        file_ids = []
        objects = {}

        for item in values:
            if isinstance(
                item,
                StoredFile,
            ):
                objects[item.pk] = item
                file_ids.append(
                    item.pk,
                )
                continue

            file_id = self.extract_id(
                item,
            )

            if file_id is None:
                continue

            file_ids.append(
                file_id,
            )

        missing_ids = [
            file_id
            for file_id in file_ids
            if file_id not in objects
        ]

        if missing_ids:
            objects.update(
                StoredFile.objects.in_bulk(
                    missing_ids,
                ),
            )

        result = []
        seen = set()

        for file_id in file_ids:
            if file_id in seen:
                continue

            file = objects.get(
                file_id,
            )

            if file is None:
                continue

            seen.add(
                file_id,
            )

            result.append(
                self.serialize_object(
                    file,
                ),
            )

        return result

    def serialize_single(
        self,
        value,
    ):
        if isinstance(
            value,
            StoredFile,
        ):
            return self.serialize_object(
                value,
            )

        file_id = self.extract_id(
            value,
        )

        if file_id is None:
            return None

        try:
            file = StoredFile.objects.get(
                pk=file_id,
            )
        except StoredFile.DoesNotExist:
            return None

        return self.serialize_object(
            file,
        )

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):
        """
        Преобразование входного значения формы в ID.

        Этот метод оставлен совместимым с normalize().
        """

        if value in (
            None,
            "",
            [],
        ):
            return (
                []
                if field.is_multiple
                else None
            )

        if field.is_multiple:
            result = []

            for item in self.ensure_list(
                value,
            ):
                file_id = self.extract_id(
                    item,
                )

                if file_id is None:
                    continue

                if file_id not in result:
                    result.append(
                        file_id,
                    )

            return result

        return self.extract_id(
            value,
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
            "url": self.get_file_url(
                file,
            ),
        }

    def get_file_url(
        self,
        file,
    ):
        stored_file = getattr(
            file,
            "file",
            None,
        )

        if not stored_file:
            return None

        try:
            return stored_file.url
        except (
            ValueError,
            AttributeError,
        ):
            return None

    # =====================================================
    # HELPERS
    # =====================================================

    def ensure_list(
        self,
        value,
    ):
        if isinstance(
            value,
            QuerySet,
        ):
            return list(
                value,
            )

        if isinstance(
            value,
            (
                list,
                tuple,
                set,
            ),
        ):
            return list(
                value,
            )

        return [
            value,
        ]

    def extract_id(
        self,
        value: Any,
    ):
        if isinstance(
            value,
            StoredFile,
        ):
            return value.pk

        if isinstance(
            value,
            dict,
        ):
            value = (
                value.get("id")
                or value.get("value")
                or value.get("pk")
            )

        try:
            file_id = int(
                value,
            )
        except (
            TypeError,
            ValueError,
        ):
            return None

        if file_id <= 0:
            return None

        return file_id