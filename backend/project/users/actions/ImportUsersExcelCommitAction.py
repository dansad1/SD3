from django.core.exceptions import ValidationError

from backend.engine.import_export.excel.BaseExcelAction import BaseExcelAction
from backend.project.users.entities.UserEntity import (
    UserEntity,
)


class ImportUsersExcelCommitAction(
    BaseExcelAction,
):

    code = "users.import.commit"

    permission = "users.create"

    entity_class = UserEntity

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        rows = payload.get(
            "rows",
        )

        if rows is None:
            raise ValidationError({
                "rows": [
                    "Нет данных для импорта",
                ],
            })

        return self.get_service(
            request,
        ).commit(
            rows,
        )