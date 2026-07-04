from django.core.exceptions import ValidationError
from openpyxl import load_workbook


class ExcelReader:

    def __init__(
        self,
        max_rows=5000,
    ):
        self.max_rows = max_rows

    def read(
        self,
        file,
    ):
        workbook = load_workbook(
            file,
            read_only=True,
            data_only=True,
        )

        sheet = workbook.active

        rows = list(
            sheet.iter_rows(
                values_only=True,
            )
        )

        if len(rows) < 3:
            raise ValidationError(
                "Файл пустой",
            )

        headers = [
            str(value).strip()
            if value is not None
            else ""
            for value in rows[0]
        ]

        data_rows = rows[2:]

        if len(data_rows) > self.max_rows:
            raise ValidationError(
                "Слишком много строк",
            )

        return {
            "headers": headers,
            "rows": data_rows,
        }