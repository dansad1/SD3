from django.core.exceptions import ValidationError

from backend.engine.import_export.excel.BaseExcelAction import BaseExcelAction
from backend.project.users.entities.UserEntity import (
    UserEntity,
)


class ImportUsersExcelPreviewAction(
    BaseExcelAction,
):

    code = "users.import.preview"

    permission = "users.create"

    entity_class = UserEntity

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        file = request.FILES.get(
            "file",
        )

        if file is None:
            raise ValidationError({
                "file": [
                    "Файл обязателен",
                ],
            })

        if not file.name.lower().endswith(
            ".xlsx",
        ):
            raise ValidationError({
                "file": [
                    "Поддерживаются только .xlsx",
                ],
            })

        return self.get_service(
            request,
        ).preview(
            file,
        )