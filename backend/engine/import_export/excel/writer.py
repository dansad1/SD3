from ..exporter import EntityExporter
from .workbook import ExcelWorkbook


class ExcelWriter:

    def __init__(
        self,
        service,
    ):
        self.service = service

        self.exporter = EntityExporter(
            service,
        )

    def export(
        self,
        queryset,
    ):
        data = self.exporter.export_queryset(
            queryset,
        )

        workbook = ExcelWorkbook(
            self.service.entity.entity,
        )

        workbook.write_headers(
            data["headers"],
        )

        workbook.write_rows(
            data["rows"],
        )

        return workbook

    def export_response(
        self,
        queryset,
    ):
        workbook = self.export(
            queryset,
        )

        return workbook.to_response(
            f"{self.service.entity.entity}.xlsx",
        )

    def template(
        self,
    ):
        data = self.exporter.export_template()

        workbook = ExcelWorkbook(
            self.service.entity.entity,
        )

        workbook.write_headers(
            data["headers"],
        )

        return workbook

    def template_response(
        self,
    ):
        workbook = self.template()

        return workbook.to_response(
            f"{self.service.entity.entity}_template.xlsx",
        )